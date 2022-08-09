import httpx
import json
import time
import random
import captchatools
import sys
import pystyle
import threading
import queue
from plugins import main_menu

with open("files/config.json") as conf: config = json.load(conf)
CAPTCHA_SERVICE = config["Captcha Stuff"]["Captcha Service"]
CAPTCHA_KEY = config["Captcha Stuff"]["Captcha Service ApiKey"]
SITE_KEY = config["Captcha Stuff"]["Site Key"]

PHONE_SERVICE = config["Phone Stuff"]["Phone Service"]
APIKEY = config["Phone Stuff"]["Phone Service ApiKey"]
COUNTRY = config["Phone Stuff"]["Phone Country ID"]

def print_main_menu(): return main_menu.logo()
def verify(total_threads, thread_index, proxy_type, tzid=None, number=None):
    lock = threading.Lock()
    useragent = None
    with open("files/useragents.txt") as ua_file:
        useragents = ua_file.readlines()
        useragent = random.choice(useragents).strip()

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
        token_file.seek(0)
        lines, line, tokencombo = token_file.readlines(), None, None

        for i, line in enumerate(lines):
            if i%total_threads == thread_index:
                tokencombo = line
                break
        
        if ":" in tokencombo:  
            token, password = tokencombo.split(":")
        else: 
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
        "user-agent": useragent,
        "x-debug-options": "bugReporterEnabled",
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwMC4wLjQ4OTYuNjAgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjEwMC4wLjQ4OTYuNjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTMyNjQ3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
    }

    fivesim_headers = {
        "Authorization": f"Bearer {APIKEY}",
        "Accept": "application/json",
    }

    check_fivesim = httpx.get(f"https://5sim.net/v1/user/profile/profile", headers=fivesim_headers)
    if check_fivesim.status_code == 401:
        pystyle.Write.Print("\t[-] Could not authenticate on 5sim with the provided API-Key. Please update files/config.json!\n", pystyle.Colors.yellow, interval=0), sys.exit(69)

    try: check_token = httpx.get("https://discord.com/api/v9/users/@me", headers=headers, proxies=proxy_auth if proxy_type != "" else None)
    except httpx.ProxyError: check_token = httpx.get("https://discord.com/api/v9/users/@me", headers=headers, proxies=None)
    
    try:
        if check_token.json()["message"] == "401: Unauthorized":
            with open("files/invalidtoken.txt", "a+") as invalid_file:
                invalid_file.write(tokencombo)
                pystyle.Write.Print(f"\t[-] Invalid Token: {token}!\n", pystyle.Colors.red, interval=0)

            with open("files/tokens.txt", "a+") as token_file:
                lines = token_file.readlines()
                token_file.seek(0)
                for item in lines:
                    if item != tokencombo: token_file.write(f"{item}\n")
                token_file.truncate()

    except KeyError:
        if "id" in check_token.json():
            pystyle.Write.Print(f"\t[+] Valid Token {token}!\n", pystyle.Colors.green, interval=0), time.sleep(.3)

        if PHONE_SERVICE == "onlinesim":
            if type(COUNTRY) is int: pass
            elif type(COUNTRY) is str: COUNTRY == int(COUNTRY)

        if PHONE_SERVICE == "5sim":
            if type(COUNTRY) is str: pass
            elif type(COUNTRY) is int: COUNTRY == str(COUNTRY)

        if PHONE_SERVICE == "onlinesim":
            resp1 = httpx.get(f"https://onlinesim.ru/api/getNum.php?apikey={APIKEY}&service=discord&number=true&country={str(COUNTRY)}")

            while resp1.json()["response"] == "INTERVAL_CONCURRENT_REQUESTS_ERROR":
                resp1 = httpx.get(f"https://onlinesim.ru/api/getNum.php?apikey={APIKEY}&service=discord&number=true&country={str(COUNTRY)}")
                time.sleep(4)
            try:
                if "tzid" or "id" in resp1.json():
                    tzid, number = resp1.json()["tzid"], resp1.json()["number"]
                    pystyle.Write.Print(f"\t[+] Sucessfully got Number {number}\n", pystyle.Colors.green, interval=0)
            except KeyError:
                if resp1.json()["response"] == "NO_NUMBER":
                    pystyle.Write.Print(f"\t[-] No Number Available for the selected country. Update files/config.json!\n", pystyle.Colors.red, interval=0), sys.exit(69)
                            
            if resp1.json()["response"] == "ACCOUNT_BLOCKED": pystyle.Write.Print(f"[-] Your Account has been blocked. Please create a new onlinesim account & use your new API Key!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "ERROR_WRONG_KEY": pystyle.Write.Print("[-] Wrong api key provided!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "ERROR_NO_KEY": pystyle.Write.Print("[-] We couldn't find a API Key!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "ERROR_NO_SERVICE": pystyle.Write.Print("[-] The Service wasn't specified!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "REQUEST_NOT_FOUND": pystyle.Write.Print("[-] The API method was not specified!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "API_ACCESS_DISABLED": pystyle.Write.Print("[-] Your API Access has been disabled!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "API_ACCESS_IP": pystyle.Write.Print("[-] The Access from this IP has been disabled in your Profile!\n", pystyle.Colors.red, interval=0), sys.exit(1)
            elif resp1.json()["response"] == "WARNING_LOW_BALANCE": pystyle.Write.Print("[-] This order can't be placed, the Account Balance is too low!\n", pystyle.Colors.red, interval=0), sys.exit(1)

        elif PHONE_SERVICE == "5sim":
            resp1 = httpx.get(f"https://5sim.net/v1/user/buy/activation/{COUNTRY}/any/discord", headers=fivesim_headers)
            if "id" in resp1.json(): tzid, number = resp1.json()["id"], resp1.json()["phone"]

        lock.acquire()
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
            waitcount = 0
            if PHONE_SERVICE == "onlinesim":
                resp3 = httpx.get(f"https://onlinesim.ru/api/getState.php?apikey={APIKEY}&tzid={tzid}&message_to_code=1")
                try:
                    if resp3.json()[0]["response"] == "WARNING_NO_NUMS": pystyle.Write.Print("[*] No matching numbers found!\n", pystyle.Colors.yellow, interval=0)
                    elif resp3.json()[0]["response"] == "TZ_INPOOL": pystyle.Write.Print("[*] Waiting for a number to be dedicated to the operation!\n", pystyle.Colors.yellow, interval=0)
                    elif resp3.json()[0]["response"] == "TZ_OVER_EMPTY": pystyle.Write.Print("[*] SMS Code did not arrive within the specified time!\n", pystyle.Colors.yellow, interval=0)
                    elif resp3.json()[0]["response"] == "TZ_OVER_OK": pystyle.Write.Print("[*] The operation has been completed!\n", pystyle.Colors.yellow, interval=0)
                    elif resp3.json()[0]["response"] == "ERROR_NO_TZID": pystyle.Write.Print("[*] The tzid is not specified!\n", pystyle.Colors.yellow, interval=0)
                    elif resp3.json()[0]["response"] == "ERROR_NO_OPERATIONS": pystyle.Write.Print("[*] No operations found!\n", pystyle.Colors.yellow, interval=0)
                    elif resp3.json()[0]["response"] == "ACCOUNT_IDENTIFICATION_REQUIRED": pystyle.Write.Print("You have to go through an identification process: to order a messenger - in any way, for forward - on the passport!\n", pystyle.Colors.yellow, interval=0)
                except KeyError: pass

                while resp3.json()[0]["response"] == "TZ_NUM_WAIT":
                    waitcount = waitcount + 1
                    if waitcount >= 15:
                        pystyle.Write.Print(f"\t[-] Phone Number {number} is banned by Discord!\n", pystyle.Colors.red, interval=0)
                        verify(total_threads, thread_index, proxy_type)
                        break
                        
                    pystyle.Write.Print(f"\t[*] Discord havn't sent the SMS so far... {waitcount}/15!\n", pystyle.Colors.yellow, interval=0)
                    resp3 = httpx.get(f"https://onlinesim.ru/api/getState.php?apikey={APIKEY}&tzid={tzid}&message_to_code=1")
                    time.sleep(3)
                
                try:    
                    if resp3.json()[0]["response"] == "TZ_NUM_ANSWER":
                        try:
                            verify_code = resp3.json()[0]["msg"]
                            pystyle.Write.Print(f"\t[*] Found Verificationcode: {verify_code}, sending it to Discord...\n", pystyle.Colors.yellow, interval=0)
                            data2 = {"phone": number, "code": verify_code}
                            
                            try: resp4 = httpx.post("https://discord.com/api/v9/phone-verifications/verify", json=data2, headers=headers, proxies=proxy_auth if proxy_type != "" else None)
                            except httpx.ProxyError: resp4 = httpx.post("https://discord.com/api/v9/phone-verifications/verify", json=data2, headers=headers, proxies=None)
                            try: phone_token = resp4.json()["token"]
                            except KeyError: phone_token = None
                            
                            data3 = {"change_phone_reason": "user_settings_update", "password": password, "phone_token": phone_token}
                            httpx.post("https://discord.com/api/v9/users/@me/phone", json=data3, headers=headers)
                            
                            with open("files/verifiedtoken.txt", "a+") as verified_file: verified_file.write(tokencombo + "\n")
                            pystyle.Write.Print(f"\t[+] Successfully verified {token} with {number}!\n", pystyle.Colors.green, interval=0)
                            """
                            Keep the function below, if you want to automatically verify another account in the current Thread after success. 
                            Remove if you want it to stop afterwards
                            """
                            # verify(total_threads, thread_index, proxy_type)
                
                        except KeyError:
                            if resp3.json()["response"] == "TRY_AGAIN_LATER":
                                pystyle.Write.Print(f"\t[*] We sent too much requests to onlinesim.io and got ratelimited...!\n", pystyle.Colors.yellow, interval=0)
                                time.sleep(3)
                                verify(total_threads, thread_index, proxy_type)
                
                except KeyError:
                    if resp3.json()["response"] == "WARNING_NO_NUMS": pystyle.Write.Print("\t[-] No matching numbers found!\n", pystyle.Colors.red, interval=0), sys.exit(69)
                    elif resp3.json()["response"] == "ERROR_NO_TZID": pystyle.Write.Print("\t[-] The tzid is not specified!\n", pystyle.Colors.red, interval=0), sys.exit(69)
                    elif resp3.json()["response"] == "ERROR_NO_OPERATIONS": pystyle.Write.Print(f"\t[-] There are no Numbers in Stock with the code {str(COUNTRY)}. Update files/config.json!\n", pystyle.Colors.red, interval=0), sys.exit(69)
                    elif resp3.json()["response"] == "ACCOUNT_IDENTIFICATION_REQUIRED": pystyle.Write.Print("You have to go through an identification process: to order a messenger - in any way, for forward - on the passport!\n", pystyle.Colors.red, interval=0), sys.exit(69)
                    else: pystyle.Write.Print("A Unexpected Error appeared while trying to verify the Phone Number. Please open a github issue with the Error below on https://github.com/FuckingToasters/discord-phone-verifier!\n", pystyle.Colors.red, interval=0), print(resp3.json()), sys.exit(69)
            
            elif PHONE_SERVICE == "5sim":
                resp3 = httpx.get(f"https://5sim.net/v1/user/check/{tzid}", headers=fivesim_headers)
                while resp3.json()["status"] == "PENDING":
                    waitcount = waitcount + 1
                    if waitcount >= 15:
                        pystyle.Write.Print(f"\t[-] Phone Number {number} is banned by Discord!\n", pystyle.Colors.red, interval=0)
                        verify(total_threads, thread_index, proxy_type)
                        break

                    pystyle.Write.Print(f"\t[*] Discord havn't sent the SMS so far... {waitcount}/15!\n", pystyle.Colors.yellow, interval=0)
                    resp3 = httpx.get(f"https://5sim.net/v1/user/check/{tzid}", headers=fivesim_headers)
                    time.sleep(3)
        

                if resp3.json()["status"] == "RECEIVED":
                    print(resp3.text)
                    verify_code = resp3.json()["sms"]["code"]
                    pystyle.Write.Print(f"\t[*] Found Verificationcode: {verify_code}, sending it to Discord...\n", pystyle.Colors.yellow, interval=0)
                    data2 = {"phone": number, "code": verify_code}
                    
                    try: resp4 = httpx.post("https://discord.com/api/v9/phone-verifications/verify", json=data2, headers=headers, proxies=proxy_auth if proxy_type != "" else None)
                    except httpx.ProxyError: resp4 = httpx.post("https://discord.com/api/v9/phone-verifications/verify", json=data2, headers=headers, proxies=None)
                    try: phone_token = resp4.json()["token"]
                    except KeyError: phone_token = None
                    
                    data3 = {"change_phone_reason": "user_settings_update", "password": password, "phone_token": phone_token}
                    httpx.post("https://discord.com/api/v9/users/@me/phone", json=data3, headers=headers)
                    
                    with open("files/verifiedtoken.txt", "a+") as verified_file: verified_file.write(tokencombo + "\n")    
                    pystyle.Write.Print(f"\t[+] Successfully verified {token} with {number}!\n", pystyle.Colors.green, interval=0)
                    """
                    Keep the function below, if you want to automatically verify another account in the current Thread after success. 
                    Remove if you want it to stop afterwards
                    """
                    # verify(total_threads, thread_index, proxy_type)
        wait_sms()

if __name__ == "__main__":
    print_main_menu()
    with open("files/tokens.txt") as tc:
        tcline = tc.readlines()
        if tcline == []: pystyle.Write.Print("\t[-] No Token found inside files/tokens.txt!\n", pystyle.Colors.red, interval=0), sys.exit(69)

    total_threads = int(pystyle.Write.Input("\t[**] How many concurrent Threads do you want to use?: ", pystyle.Colors.cyan, interval=0))
    proxy_input = pystyle.Write.Input("\t[**] Proxy Type (http/https/socks5) | Enter nothing to use without Proxy: ", pystyle.Colors.cyan, interval=0)

    if proxy_input == "https": proxy_input = "http"
    threads = []

    try:
        for thread_index in range(int(total_threads)):
            t = threading.Thread(target=verify, args=(int(total_threads), thread_index, proxy_input, ))
            t.start()
            threads.append(t)

    except ValueError:
        print(pystyle.Write.Input("\t[**] Enter a valid Thread Number!\n", pystyle.Colors.red, interval=0))
        sys.exit(1)
