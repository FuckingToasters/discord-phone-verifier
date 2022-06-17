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

def print_main_menu(): return main_menu.logo()
def verify(proxy_type, tzid=None, number=None):
    with open("files/proxies.txt", "r") as proxy_file:
        proxies = proxy_file.read().splitlines()
        try:
            proxy_split = random.choice(proxies).split(":")
            host_name, port, username, password = proxy_split[0], proxy_split[1], proxy_split[2], proxy_split[3]
            proxy_formatted = f"://{username}:{password}@{host_name}:{port}"
            if proxy_type != "": proxy_auth = {"all://": proxy_formatted}
            else: proxy_auth = {"all://": None}
        except IndexError: proxy_auth = {"all://": None}


    with open("files/tokens.txt", "r+") as token_file:
        try: line = random.choice(token_file.readlines()).split(":")
        except IndexError: pystyle.Write.Print("\t[*] Make sure that the Tokens inside tokens.txt are formatted correctly (token:password)!\n", pystyle.Colors.yellow, interval=0), sys.exit(1)
        token, password = line[0], line[1]
        tokencombo = line[0] + ":" + line[1]
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "content-type": "application/json",
        "cookie": "__dcfduid=8390e660ee1811ec8d3b1b6a623c7dd4; __sdcfduid=8390e661ee1811ec8d3b1b6a623c7dd4e5aec00daf4eabeda71b40dd60c7012044b50d1e3da920dd20ccda5cce8e7dba; locale=en-US,en;q=0.9",
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
    check_token = httpx.get("https://discord.com/api/v9/users/@me", headers=headers, proxies=proxy_auth)
    try:
        if check_token.json()["message"] == "401: Unauthorized":
            with open("files/invalidtoken.txt", "w+") as invalid_file:
                invalid_file.write(tokencombo + "\n")
                pystyle.Write.Print(f"\t[-] Invalid Token: {token}!\n", pystyle.Colors.red, interval=0)

            with open("files/tokens.txt", "r+") as token_file:
                lines = token_file.readlines()
                token_file.seek(0)
                for item in lines:
                    if item != tokencombo: token_file.write(item)
                token_file.truncate()
            verify()

    except KeyError:
        if "id" in check_token.json():
            pystyle.Write.Print(f"\t[+] Valid Token {token}!\n", pystyle.Colors.green, interval=0)

            resp1 = httpx.get(f"https://onlinesim.ru/api/getNum.php?apikey={APIKEY}&service=discord&number=true&country={COUNTRY}")
            if "tzid" in resp1.json():
                pystyle.Write.Print(f"\t[+] Sucessfully got a Number from https://onlinesim.ru!\n", pystyle.Colors.green, interval=0)
                tzid, number = resp1.json()["tzid"], resp1.json()["number"]

            if resp1.json()["response"] == "ACCOUNT_BLOCKED": pystyle.Write.Print(f"\t[-] Your Account has been blocked. Please create a new onlinesim account & use your new API Key!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "ERROR_WRONG_KEY": pystyle.Write.Print("\t[-] Wrong api key provided!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "ERROR_NO_KEY": pystyle.Write.Print("\t[-] We couldn't find a API Key!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "ERROR_NO_SERVICE": pystyle.Write.Print("\t[-] The Service wasn't specified!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "REQUEST_NOT_FOUND": pystyle.Write.Print("\t[-] The API method was not specified!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "API_ACCESS_DISABLED": pystyle.Write.Print("\t[-] Your API Access has been disabled!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "API_ACCESS_IP": pystyle.Write.Print("\t[-] The Access from this IP has been disabled in your Profile!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "WARNING_LOW_BALANCE": pystyle.Write.Print("\t[-] This order can't be placed, the Account Balance is too low!\n", pystyle.Colors.red, interval=0), sys.exit(1)


            pystyle.Write.Print("\t[*] Solving captcha... please be patient!\n", pystyle.Colors.yellow, interval=0)
            solver = captchatools.captcha_harvesters(solving_site=CAPTCHA_SERVICE, api_key=CAPTCHA_KEY, sitekey="f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34", captcha_url="https://discord.com/api/v9/users/@me/phone")
            captcha_token = solver.get_token()
            data1 = {"captcha_key": captcha_token, "change_phone_reason": "user_settings_update", "phone": number}
            resp2 = httpx.post("https://discord.com/api/v9/users/@me/phone", json=data1, headers=headers, proxies=proxy_auth)

            if json.decoder.JSONDecodeError: pass
            if resp2.status_code == 204:
                pystyle.Write.Print("\t[+] Successfully requested verification code!\n", pystyle.Colors.green, interval=0)
            time.sleep(4)

            resp3 = httpx.get(f"https://onlinesim.ru/api/getState.php?apikey={APIKEY}&tzid={tzid}&message_to_code=1")
            if resp3.json()[0]["response"] == "WARNING_NO_NUMS": pystyle.Write.Print("\t[*] No matching numbers found!\n", pystyle.Colors.yellow, interval=0)
            elif resp3.json()[0]["response"] == "TZ_INPOOL": ppystyle.Write.Print("\t[*] Waiting for a number to be dedicated to the operation!\n", pystyle.Colors.yellow, interval=0)
            elif resp3.json()[0]["response"] == "TZ_NUM_ANSWER": pystyle.Write.Print("\t[*] SMS Code has arrived!\n", pystyle.Colors.yellow, interval=0)
            elif resp3.json()[0]["response"] == "TZ_OVER_EMPTY": pystyle.Write.Print("\t[*] SMS Code did not arrive within the specified time!\n", pystyle.Colors.yellow, interval=0)
            elif resp3.json()[0]["response"] == "TZ_OVER_OK": pystyle.Write.Print("\t[*] The operation has been completed!\n", pystyle.Colors.yellow, interval=0)
            elif resp3.json()[0]["response"] == "ERROR_NO_TZID": pystyle.Write.Print("\t[*] The tzid is not specified!\n", pystyle.Colors.yellow, interval=0)
            elif resp3.json()[0]["response"] == "ERROR_NO_OPERATIONS": pystyle.Write.Print("\t[*] No operations found!\n", pystyle.Colors.yellow, interval=0)
            elif resp3.json()[0]["response"] == "ACCOUNT_IDENTIFICATION_REQUIRED": pystyle.Write.Print("\tYou have to go through an identification process: to order a messenger - in any way, for forward - on the passport!\n", pystyle.Colors.yellow, interval=0)

            pystyle.Write.Print("[*] Waiting for the SMS Code...!\n", pystyle.Colors.yellow, interval=0)
            while resp3.json()[0]["response"] == "TZ_NUM_WAIT":
                resp3 = httpx.get(f"https://onlinesim.ru/api/getState.php?apikey={APIKEY}&tzid={tzid}&message_to_code=1")
                time.sleep(4)

            verify_code = resp3.json()[0]["msg"]
            pystyle.Write.Print(f"\t[*] Found Verificationcode: {verify_code}, sending it to Discord...\n", pystyle.Colors.yellow, interval=0)
            if resp3.json()[0]["response"] == "ERROR_WRONG_KEY": pass

            data2 = {"phone": number, "code": verify_code}
            resp4 = httpx.post("https://discord.com/api/v9/phone-verifications/verify", json=data2, headers=headers, proxies=proxy_auth)
            phone_token = resp4.json()["token"]

            data3 = {"change_phone_reason": "user_settings_update", "password": password, "phone_token": phone_token}
            httpx.post("https://discord.com/api/v9/users/@me/phone", json=data3, headers=headers)
            pystyle.Write.Print("\t[+] Successfully verified Account by Phone!\n", pystyle.Colors.green, interval=0)
            with open("files/verifiedtoken.txt", "w+") as verified_file:
                verified_file.write(tokencombo + "\n")

if __name__ == "__main__":
    print_main_menu()
    session_input = pystyle.Write.Input("[**] How many concurrent Threads do you want to use?: ", pystyle.Colors.cyan, interval=0).lower()
    proxy_input = pystyle.Write.Input("\t[**] Proxy Type (http/https/socks5) | Enter nothing to use without Proxy: ", pystyle.Colors.cyan, interval=0).lower()
    threads = []
    try:
        for _ in range(int(session_input)):
            t = threading.Thread(target=verify, args=(proxy_input,))
            t.start()
            threads.append(t)

    except ValueError:
        print(pystyle.Write.Input("\t[**] Enter a valid Thread Number!\n", pystyle.Colors.red, interval=0).lower())
        sys.exit(1)