import json
import httpx
import pystyle
import sys
import time
import pystyle

from plugins.configuration.load import config
CAPTCHASERVICE, CAPTCHAKEY, SITEKEY, _, _, _, _, _, _, _, _, _, _ = config().loadconfig()
BASEURL = "https://api.capsolver.com"
HEADERS = {"Content-Type": "application/json"}
TASKID = None

# from plugins.filesupport.proxy import loadproxyclass
# _, hostname, port, username, password = loadproxyclass().loadproxy(proxytype="http")


class Solver:
    async def createtask():
        # if hostname is None and port is None:
        payload = {
            "clientKey": CAPTCHAKEY,
            "isEnterprise": True,
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
            "task": {
                "type":"HCaptchaTurboTaskProxyLess",
                "websiteURL":"https://discord.com/api/v9/users/@me/phone",
                "websiteKey": SITEKEY
            }
        }

        """

        elif hostname is not None and port is not None:
            payload = {
                "clientKey": CAPTCHAKEY,
                "task": {
                        "type":"HCaptchaTask",
                        "websiteURL": "https://discord.com/api/v9/users/@me/phone",
                        "websiteKey": SITEKEY,
                        "proxyType": "http",
                        "proxyAddress": hostname,
                        "proxyPort": int(port),
                        "proxyLogin": username,
                        "proxyPassword": password,
                        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
                        "isEnterprise": True
                }
            }
        """

        with httpx.Client(headers=HEADERS) as client:
            response = client.post(f"{BASEURL}/createTask", json=payload).json()

        if "taskId" in response:
            TASKID = response["taskId"]

        elif "errorDescription" in response:
            if response["errorDescription"] == "clientKey error":
                pystyle.Write.Print(f"\t[-] Invalid Captcha Solving API Key for {CAPTCHASERVICE} is set!\n", pystyle.Colors.red, interval=0), time.sleep(2), sys.exit(0)

            elif response["errorDescription"] == "Your service balance is insufficient.":
                pystyle.Write.Print(f"\t[-] Captcha Solving Balance on {CAPTCHASERVICE} is too low to complete this action!\n", pystyle.Colors.red, interval=0), time.sleep(2), sys.exit(0)

            elif response["errorDescription"] == "proxy cannot connect to the server.":
                pystyle.Write.Print(f"\t[-] Proxy cannot connect to Captcha Solving Server!\n", pystyle.Colors.red, interval=0), time.sleep(2), sys.exit(0)

        return TASKID


    async def solution():
        TASKID = await Solver.createtask()
        CAPTCHATOKEN = None
        with httpx.Client(headers=HEADERS) as client:
            response = client.post(f"{BASEURL}/getTaskResult", json={"clientKey": CAPTCHAKEY, "taskId": TASKID}).json()

            if "status" in response:
                while response["status"] == "processing":
                    response = client.post(f"{BASEURL}/getTaskResult", json={"clientKey": CAPTCHAKEY, "taskId": TASKID}).json()
                    time.sleep(.3)

        if response["status"] == "ready":
            CAPTCHATOKEN = response["solution"]["gRecaptchaResponse"]
            pystyle.Write.Print(f"\t[+] Successfully solved captcha with Service {CAPTCHASERVICE}!\n", pystyle.Colors.green, interval=0)

        elif response["status"] == "failed":
            if response["errorDescription"] == "Captcha not recognized":
                pystyle.Write.Print(f"\t[-] Captcha wasn't recognized!, retrying...\n", pystyle.Colors.red, interval=0)
                await Solver.createtask()

        return CAPTCHATOKEN


