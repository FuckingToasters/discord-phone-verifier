import httpx
import json
import time
import captchatools
import sys
import random
import pystyle
import threading
from plugins import main_menu

with open("files/config.json") as conf: config = json.load(conf)
APIKEY = config["Phone Stuff"]["Phone Service ApiKey"]
COUNTRY = config["Phone Stuff"]["Phone Country ID"]
CAPTCHA_SERVICE = config["Captcha Stuff"]["Captcha Service"]
CAPTCHA_KEY = config["Captcha Stuff"]["Captcha Service ApiKey"]
SITE_KEY = config["Captcha Stuff"]["Site Key"]

def print_main_menu(): return main_menu.logo()
def verify(proxy_type, tzid=None, number=None):
    if CAPTCHA_SERVICE == "capmonster":
        pystyle.Write.Print("\t[-] Seems like you are using capmonster. Please change the Captcha Service in files/config.json (Capmonster is flagged)!\n", pystyle.Colors.red, interval=0)
        sys.exit(69)
        
    with open("files/proxies.txt", "r") as proxy_file:
        proxies = proxy_file.read().splitlines()
        proxy_split = "None"
        for proxy in proxies:
            proxy_split = proxy.split(":")
        try:
            host_name, port, username, password = proxy_split[0], proxy_split[1], proxy_split[2], proxy_split[3]
            proxy_formatted = f"{proxy_type}://{username}:{password}@{host_name}:{port}"
            if proxy_type != "": proxy_auth = {"all://": proxy_formatted}
            else: proxy_auth = {"all://": None}

        except IndexError:
            try:
                host_name, port = proxy_split[0], proxy_split[1]
                proxy_formatted = f"{proxy_type}://{host_name}:{port}"
                if proxy_type != "": proxy_auth = {"all://": proxy_formatted}
                else: proxy_auth = {"all://": None}

            except IndexError:
                pystyle.Write.Print("\t[*] Proxies inside files/proxies.txt are not formatted correctly (IP:PORT or IP:PORT:USER:PASS)!\n", pystyle.Colors.yellow, interval=0)
                proxy_auth = {"all://": None}

    with open("files/tokens.txt", "r+") as token_file:
        try:
            lines = token_file.read().splitlines()
            line = "None"
            for line in lines:
                line = line.split(":")
            token, password = line[0], line[1]
            tokencombo = line[0] + ":" + line[1]
        except IndexError:
            pystyle.Write.Print("\t[*] Tokens inside tokens.txt are not formatted correctly (token:password)!\n", pystyle.Colors.yellow, interval=0)
            sys.exit(1)

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "content-type": "application/json",
        "origin": "https://discord.com",
        "referer": "https://discord.com/channels/@me",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
        "x-debug-options": "bugReporterEnabled",
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwMC4wLjQ4OTYuNjAgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjEwMC4wLjQ4OTYuNjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTMyNjQ3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
    }
    try: check_token = httpx.get("https://discord.com/api/v9/users/@me", headers=headers, proxies=proxy_auth if proxy_type != "" else None)
    except httpx.ProxyError: check_token = httpx.get("https://discord.com/api/v9/users/@me", headers=headers, proxies=None)
    
    try:
        if check_token.json()["message"] == "401: Unauthorized":
            with open("files/invalidtoken.txt", "a+") as invalid_file:
                invalid_file.write(tokencombo)
                pystyle.Write.Print(f"[-] Invalid Token: {token}!\n", pystyle.Colors.red, interval=0)

            with open("files/tokens.txt", "a+") as token_file:
                lines = token_file.readlines()
                token_file.seek(0)
                for item in lines:
                    if item != tokencombo: token_file.write(item)
                token_file.truncate()
            verify(proxy_type=proxy_type)

    except KeyError:
        lock = threading.Lock()
        if "id" in check_token.json():
            pystyle.Write.Print(f"\t[+] Valid Token {token}!\n", pystyle.Colors.green, interval=0)
            resp1 = httpx.get(f"https://onlinesim.ru/api/getNum.php?apikey={APIKEY}&service=discord&number=true&country={COUNTRY}")

            while resp1.json()["response"] == "INTERVAL_CONCURRENT_REQUESTS_ERROR":
                resp1 = httpx.get(f"https://onlinesim.ru/api/getNum.php?apikey={APIKEY}&service=discord&number=true&country={COUNTRY}")
                time.sleep(4)

            if "tzid" in resp1.json():
                tzid, number = resp1.json()["tzid"], resp1.json()["number"]
                pystyle.Write.Print(f"\t[+] Sucessfully got Number {number} from https://onlinesim.ru!\n", pystyle.Colors.green, interval=0)

            lock.acquire()
            if resp1.json()["response"] == "ACCOUNT_BLOCKED": pystyle.Write.Print(f"[-] Your Account has been blocked. Please create a new onlinesim account & use your new API Key!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "ERROR_WRONG_KEY": pystyle.Write.Print("[-] Wrong api key provided!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "ERROR_NO_KEY": pystyle.Write.Print("[-] We couldn't find a API Key!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "ERROR_NO_SERVICE": pystyle.Write.Print("[-] The Service wasn't specified!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "REQUEST_NOT_FOUND": pystyle.Write.Print("[-] The API method was not specified!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "API_ACCESS_DISABLED": pystyle.Write.Print("[-] Your API Access has been disabled!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "API_ACCESS_IP": pystyle.Write.Print("[-] The Access from this IP has been disabled in your Profile!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "WARNING_LOW_BALANCE": pystyle.Write.Print("[-] This order can't be placed, the Account Balance is too low!\n", pystyle.Colors.red, interval=0), sys.exit(1)

            pystyle.Write.Print("\t[*] Solving captcha... please be patient!\n", pystyle.Colors.yellow, interval=0)
            solver = captchatools.captcha_harvesters(solving_site=CAPTCHA_SERVICE, api_key=CAPTCHA_KEY, captcha_type="hcaptcha", sitekey=SITE_KEY, captcha_url="https://discord.com/api/v9/users/@me/phone")
            captcha_token = solver.get_token()
            lock.release()

            data1 = {"captcha_key": captcha_token, "change_phone_reason": "user_settings_update", "phone": number}
            try: resp2 = httpx.post("https://discord.com/api/v9/users/@me/phone", json=data1, headers=headers, proxies=proxy_auth if proxy_type != "" else None)
            except httpx.ProxyError: resp2 = httpx.post("https://discord.com/api/v9/users/@me/phone", json=data1, headers=headers, proxies=None)

            if json.decoder.JSONDecodeError: pass
            if resp2.status_code == 204: pystyle.Write.Print("\t[+] Successfully requested verification code!\n", pystyle.Colors.green, interval=0)

            def wait_sms():
                resp3 = httpx.get(f"https://onlinesim.ru/api/getState.php?apikey={APIKEY}&tzid={tzid}&message_to_code=1")
                try:
                    if resp3.json()[0]["response"] == "WARNING_NO_NUMS": pystyle.Write.Print("[*] No matching numbers found!\n", pystyle.Colors.yellow, interval=0)
                    elif resp3.json()[0]["response"] == "TZ_INPOOL": pystyle.Write.Print("[*] Waiting for a number to be dedicated to the operation!\n", pystyle.Colors.yellow, interval=0)
                    # elif resp3.json()[0]["response"] == "TZ_NUM_ANSWER": pystyle.Write.Print("[*] SMS Code has arrived!\n", pystyle.Colors.yellow, interval=0)
                    elif resp3.json()[0]["response"] == "TZ_OVER_EMPTY": pystyle.Write.Print("[*] SMS Code did not arrive within the specified time!\n", pystyle.Colors.yellow, interval=0)
                    elif resp3.json()[0]["response"] == "TZ_OVER_OK": pystyle.Write.Print("[*] The operation has been completed!\n", pystyle.Colors.yellow, interval=0)
                    elif resp3.json()[0]["response"] == "ERROR_NO_TZID": pystyle.Write.Print("[*] The tzid is not specified!\n", pystyle.Colors.yellow, interval=0)
                    elif resp3.json()[0]["response"] == "ERROR_NO_OPERATIONS": pystyle.Write.Print("[*] No operations found!\n", pystyle.Colors.yellow, interval=0)
                    elif resp3.json()[0]["response"] == "ACCOUNT_IDENTIFICATION_REQUIRED": pystyle.Write.Print("You have to go through an identification process: to order a messenger - in any way, for forward - on the passport!\n", pystyle.Colors.yellow, interval=0)
                except KeyError: pass

                pystyle.Write.Print("\t[*] Waiting for the SMS Code...!\n", pystyle.Colors.yellow, interval=0)
                timeout = time.time() + 120
                try:
                    while timeout >= time.time():
                        while resp3.json()[0]["response"] == "TZ_NUM_WAIT":
                            resp3 = httpx.get(f"https://onlinesim.ru/api/getState.php?apikey={APIKEY}&tzid={tzid}&message_to_code=1")
                            time.sleep(.5)

                        if resp3.json()[0]["response"] == "TZ_NUM_ANSWER":
                            global verify_code
                            verify_code = resp3.json()[0]["msg"]
                            pystyle.Write.Print(f"\t[*] Found Verificationcode: {verify_code}, sending it to Discord...\n", pystyle.Colors.yellow, interval=0)
                            data2 = {"phone": number, "code": verify_code}
                            try: resp4 = httpx.post("https://discord.com/api/v9/phone-verifications/verify", json=data2, headers=headers, proxies=proxy_auth if proxy_type != "" else None)
                            except httpx.ProxyError: resp4 = httpx.post("https://discord.com/api/v9/phone-verifications/verify", json=data2, headers=headers, proxies=None)
                            try: phone_token = resp4.json()["token"]
                            except KeyError: phone_token = None

                            data3 = {"change_phone_reason": "user_settings_update", "password": password, "phone_token": phone_token}
                            httpx.post("https://discord.com/api/v9/users/@me/phone", json=data3, headers=headers)
                            with open("files/verifiedtoken.txt", "a+") as verified_file: verified_file.write(tokencombo)

                            with open("files/tokens.txt", "a+") as token_file:
                                lines = token_file.readlines()
                                for item in lines:
                                    if item != tokencombo: token_file.write(item)
                                token_file.truncate()
                            pystyle.Write.Print(f"\t[+] Successfully verified {token} with {number}!\n", pystyle.Colors.green, interval=0)
                        if resp3.json()[0]["response"] == "ERROR_WRONG_KEY": pass
                        break

                except KeyError:
                    if resp3.json()["response"] == "TRY_AGAIN_LATER":
                        timeout = time.time() + 30
                        pystyle.Write.Print(f"\t[*] Temporarily unable to perform the request, retrying for 30 Seconds...!\n", pystyle.Colors.yellow, interval=0)
                        while timeout >= time.time(): time.sleep(.5), wait_sms() # try to get a new sms for 30 seconds
                        while timeout < time.time(): verify(proxy_type=proxy_type) # if 30 seconds have passed, run the script again in the same thread (remove this line to exit the loop)

                if resp3.json()[0]["response"] != "TZ_NUM_ANSWER":
                    pystyle.Write.Print(f"\t[*] Timeout, couldn't get the SMS within 2 Minutes. rerunning...\n", pystyle.Colors.yellow, interval=0)
                    verify(proxy_type=proxy_type)
            wait_sms()

if __name__ == "__main__":
    print_main_menu()
    session_input = pystyle.Write.Input("\t[**] How many concurrent Threads do you want to use?: ", pystyle.Colors.cyan, interval=0)
    proxy_input = pystyle.Write.Input("\t    [**] Proxy Type (http/https/socks5) | Enter nothing to use without Proxy: ", pystyle.Colors.cyan, interval=0)
    if proxy_input == "https": proxy_input = "http"
    threads = []
    try:
        for _ in range(int(session_input)):
            t = threading.Thread(target=verify, args=(proxy_input,))
            t.start()
            threads.append(t)

    except ValueError:
        print(pystyle.Write.Input("[**] Enter a valid Thread Number!\n", pystyle.Colors.red, interval=0))
        sys.exit(1)
