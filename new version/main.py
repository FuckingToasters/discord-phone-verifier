import json
import httpx
import time
import sys
import pystyle
import threading
from plugins.design import mainmenu
from plugins.filesupport.proxy import loadproxyclass
from plugins.filesupport.useragent import randomagentclass
from plugins.captcha.hcaptchasolver import bypasscaptcha
from plugins.phoneservices.vaksms import vakverification
from plugins.configuration.load import config

def print_main_menu(): return mainmenu.logo()
def verify(totalthreads, threadindex, proxytype):
    lock = threading.Lock()
    vaksms = vakverification()
    bypasscap = bypasscaptcha()
    proxyauth = loadproxyclass().loadproxy(proxytype=proxytype)
    _, _, _, PHONESERVICE, VAKAPIKEY, _, _, _ = config().loadconfig()
    USERAGENT = randomagentclass().randomagent()

    if str(PHONESERVICE).lower() != "vaksms":
        pystyle.Write.Print(f"\t[-] Only https://vak-sms.com is supported at the moment!\n", pystyle.Colors.red, interval=0), time.sleep(2), sys.exit(0)


    def gettoken():
        with open("files/tokens.txt", "r+") as tokenfile:
            tokenfile.seek(0)
            LINES = tokenfile.readlines()
            TOKENCOMBO = []

            for I, TOKENCOMBO in enumerate(LINES):
                if I%totalthreads == threadindex:
                    if ":" in TOKENCOMBO: break
            if TOKENCOMBO == []: pystyle.Write.Print(f"\t[-] No more Tokens available in files/tokens.txt!\n", pystyle.Colors.red, interval=0), time.sleep(2), sys.exit(0)
            elif ":" not in TOKENCOMBO: pystyle.Write.Print("\t[*] Tokens inside files/tokens.txt are not formatted correctly (token:password)!\n", pystyle.Colors.yellow, interval=0), sys.exit(1)
            TOKEN, PASSWORD = TOKENCOMBO.split(":")
        return TOKENCOMBO, TOKEN, PASSWORD
    TOKENCOMBO, TOKEN, PASSWORD = gettoken()

    def removetoken():
        with open("files/tokens.txt", "r+") as tokenfile:
            tokenfile.seek(0)
            LINES = tokenfile.readlines()
            if TOKENCOMBO in LINES:
                LINES.remove(TOKENCOMBO)
                tokenfile.seek(0), tokenfile.truncate(), tokenfile.writelines(LINES)
            else: pass
            # else: lock.acquire(), pystyle.Write.Print(f"\t[-] Every Token from files/tokens.txt got used. File need to be refilled!\n", pystyle.Colors.red, interval=0), lock.release(), sys.exit(1)

    HEADERS = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "authorization": TOKEN,
        "content-type": "application/json",
        "origin": "https://discord.com",
        "referer": "https://discord.com/channels/@me",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": USERAGENT,
        "x-debug-options": "bugReporterEnabled",
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwMC4wLjQ4OTYuNjAgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjEwMC4wLjQ4OTYuNjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTMyNjQ3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
    }
    
    def checktoken():
        try: response = httpx.get("https://discord.com/api/v9/users/@me", headers=HEADERS, proxies=proxyauth if proxytype != "" else None)
        except httpx.ProxyError: response = httpx.get("https://discord.com/api/v9/users/@me", headers=HEADERS, proxies=None)
    
        try:
            if response.json()["message"] == "401: Unauthorized":
                with open("files/invalidtoken.txt", "a+") as invalidfile: invalidfile.write(TOKENCOMBO)
                removetoken()
                pystyle.Write.Print(f"\t[-] Invalid Token: {TOKEN}!\n", pystyle.Colors.red, interval=0)
                verify(totalthreads, threadindex, proxytype)
        
        except KeyError:
            if "id" in response.json(): lock.acquire(), pystyle.Write.Print(f"\t[+] Valid Token {TOKEN}!\n", pystyle.Colors.green, interval=0), lock.release()
    checktoken()

    if str(PHONESERVICE).lower() == "vaksms": NUMBER, TZID = vaksms.ordernumber()

    def verifiedtoken():
        with open("files/verifiedtoken.txt", "a+") as verifiedfile: verifiedfile.write(TOKENCOMBO)
        with open("files/tokens.txt", "a+") as tokenfile:
            lines = tokenfile.readlines()
            for line in lines:
                if line.strip("\n") != TOKENCOMBO:
                    tokenfile.write(line)
        lock.acquire(), pystyle.Write.Print(f"\t[+] Successfully verified {TOKEN} with {NUMBER}!\n", pystyle.Colors.green, interval=0), lock.release()
        removetoken()
        verify(totalthreads, threadindex, proxytype)

    lock.acquire()
    pystyle.Write.Print(f"\t[+] Sucessfully got Number {NUMBER}\n", pystyle.Colors.green, interval=0)
    pystyle.Write.Print("\t[*] Solving captcha... please be patient!\n", pystyle.Colors.yellow, interval=0)
    lock.release()
    CAPTCHATOKEN = bypasscap.hcaptcha()

    data1 = {"captcha_key": CAPTCHATOKEN, "change_phone_reason": "user_settings_update", "phone": NUMBER}
    try: resp2 = httpx.post("https://discord.com/api/v9/users/@me/phone", json=data1, headers=HEADERS, proxies=proxyauth if proxytype != "" else None)
    except httpx.ProxyError: resp2 = httpx.post("https://discord.com/api/v9/users/@me/phone", json=data1, headers=HEADERS, proxies=None)
    lock.acquire()
    if resp2.status_code == 204: pystyle.Write.Print("\t[+] Successfully requested verification code!\n", pystyle.Colors.green, interval=0)
    lock.release()

    def waitsms():
        waitcount = 0
        if str(PHONESERVICE).lower() == "vaksms": smsurl = f"https://vak-sms.com/api/getSmsCode/?apiKey={VAKAPIKEY}&idNum={TZID}"
        discordurl = "https://discord.com/api/v9/users/@me/phone"
        
        smsresponse = httpx.get(smsurl, headers=None).json()
        discordresponse = httpx.get(discordurl, headers=HEADERS, proxies=proxyauth if proxytype != "" else None).json()
        while smsresponse["smsCode"] is None: 
            waitcount = waitcount + 1
            lock.acquire(), pystyle.Write.Print(f"\t[*] Discord havn't sent the SMS so far... {waitcount}/1200!\n", pystyle.Colors.yellow, interval=0), lock.release()
            smsresponse = httpx.get(smsurl, headers=None).json()
            time.sleep(.5)
            
            if waitcount % 5 == 0: # run every x time to request a new sms from discord
                data = {"phone": NUMBER, "change_phone_reason": "user_settings_update"}
                discordurl = "https://discord.com/api/v9/users/@me/phone"
                discordresponse = httpx.post(discordurl, json=data, headers=HEADERS, proxies=proxyauth if proxytype != "" else None)
            
            if waitcount >= 1200:
                lock.acquire()
                pystyle.Write.Print(f"\t[-] Discord did not sent a SMS to {NUMBER} in time! Check the Token & Proxy Quality\n", pystyle.Colors.red, interval=0)
                with open("files/failedverify.txt", "a+") as failedfile: failedfile.write(TOKENCOMBO)
                removetoken()
                if str(PHONESERVICE).lower() == "vaksms": vaksms.deletenumber()
                verify(totalthreads, threadindex, proxytype)

        verifycode = smsresponse["smsCode"]
        return verifycode
    VERIFYCODE = waitsms()

    if VERIFYCODE is not None:
        lock.acquire(), pystyle.Write.Print(f"\t[*] Found Verificationcode: {VERIFYCODE}, sending it to Discord...\n", pystyle.Colors.yellow, interval=0), lock.release()
        data2 = {"phone": NUMBER, "code": VERIFYCODE}
        
        try: resp4 = httpx.post("https://discord.com/api/v9/phone-verifications/verify", json=data2, headers=HEADERS, proxies=proxyauth if proxytype != "" else None)
        except httpx.ProxyError: resp4 = httpx.post("https://discord.com/api/v9/phone-verifications/verify", json=data2, headers=HEADERS, proxies=None)
        try: phone_token = resp4.json()["token"]
        except KeyError: phone_token = None
        
        data3 = {"change_phone_reason": "user_settings_update", "password": PASSWORD, "phone_token": phone_token}
        httpx.post("https://discord.com/api/v9/users/@me/phone", json=data3, headers=HEADERS)
        verifiedtoken()
    
    elif VERIFYCODE is None:
        lock.acquire(), pystyle.Write.Print(f"\t[-] Failed to get verification code! Rerunning...\n", pystyle.Colors.red, interval=0), lock.release()
        with open("files/failedverify.txt", "a+") as failedfile: failedfile.write(TOKENCOMBO)
        removetoken()
        verify(totalthreads, threadindex, proxytype)

if __name__ == "__main__":
    print_main_menu()

    with open("files/tokens.txt") as tc:
        tcline = tc.readlines()
        if tcline == []: pystyle.Write.Print("\t[-] No Token found inside files/tokens.txt!\n", pystyle.Colors.red, interval=0), sys.exit(69)
    
    totalthreads = int(pystyle.Write.Input("\t[**] How many concurrent Threads do you want to use?: ", pystyle.Colors.cyan, interval=0))
    proxyinput = pystyle.Write.Input("\t[**] Proxy Type (http/https/socks5) | Enter nothing to use without Proxy: ", pystyle.Colors.cyan, interval=0)
    if proxyinput == "https": proxyinput = "http"
    threads = []
    try:
        for threadindex in range(int(totalthreads)):
            t = threading.Thread(target=verify, args=(int(totalthreads), threadindex, proxyinput, ))
            t.start()
            threads.append(t)

    except ValueError:
        print(pystyle.Write.Input("\t[**] Enter a valid Thread Number!\n", pystyle.Colors.red, interval=0))
        sys.exit(1)
