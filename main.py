import json
import httpx
import tls_client # pip install tls-client
import time
import sys
import pystyle
import threading
import os
import re

from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import date
from plugins.misc.gettoken import gettokenclass
from plugins.misc.proxy import loadproxyclass
from plugins.misc.get_discord_headers import getheadersclass
from plugins.captcha.hcaptchasolver import bypasscaptcha
from plugins.phoneservices.vaksms import vakverification
from plugins.phoneservices.fivesim import fivesimverification
from plugins.phoneservices.smshub import smshubverification
from plugins.configuration.load import config

def verify(totalthreads, threadindex, proxytype):
    HEADERS = getheadersclass.getheaders(totalthreads, threadindex)
    CONFIG = list(config().loadconfig())
    CAPTCHASERVICE = CONFIG[0]
    CAPTCHAPIKEY = CONFIG[1]
    CAPTCHASITEKEY = CONFIG[2]
    PHONESERVICE = CONFIG[3]
    TOTALRETRIES = CONFIG[4]
    OPERATOR = CONFIG[5]
    VAKAPIKEY = CONFIG[6]
    VAKCOUNTRY = CONFIG[7]
    FIVESIMAPIKEY = CONFIG[8]
    FIVESIMCOUNTRY = CONFIG[9]
    SMSHUBAPIKEY = CONFIG[10]
    SMSHUBCOUNTRY = CONFIG[11]
    WEBHOOKURL = CONFIG[12]

    captcha_required = False
    lock = threading.Lock()
    vaksms = vakverification(
        TOTALTHREADS=totalthreads,
        THREADINDEX=threadindex,
        CAPTCHASERVICE=CAPTCHASERVICE,
        CAPTCHAPIKEY=CAPTCHAPIKEY,
        CAPTCHASITEKEY=CAPTCHASITEKEY,
        PHONESERVICE=PHONESERVICE,
        TOTALRETRIES=TOTALRETRIES,
        OPERATOR=OPERATOR,
        VAKAPIKEY=VAKAPIKEY,
        VAKCOUNTRY=VAKCOUNTRY,
        FIVESIMAPIKEY=FIVESIMAPIKEY,
        FIVESIMCOUNTRY=FIVESIMCOUNTRY,
        SMSHUBAPIKEY=SMSHUBAPIKEY,
        SMSHUBCOUNTRY=SMSHUBCOUNTRY,
        WEBHOOKURL=WEBHOOKURL
    )

    fivesim = fivesimverification(
        TOTALTHREADS=totalthreads,
        THREADINDEX=threadindex,
        CAPTCHASERVICE=CAPTCHASERVICE,
        CAPTCHAPIKEY=CAPTCHAPIKEY,
        CAPTCHASITEKEY=CAPTCHASITEKEY,
        PHONESERVICE=PHONESERVICE,
        TOTALRETRIES=TOTALRETRIES,
        OPERATOR=OPERATOR,
        VAKAPIKEY=VAKAPIKEY,
        VAKCOUNTRY=VAKCOUNTRY,
        FIVESIMAPIKEY=FIVESIMAPIKEY,
        FIVESIMCOUNTRY=FIVESIMCOUNTRY,
        SMSHUBAPIKEY=SMSHUBAPIKEY,
        SMSHUBCOUNTRY=SMSHUBCOUNTRY,
        WEBHOOKURL=WEBHOOKURL
    )

    smshub = smshubverification(
        TOTALTHREADS=totalthreads,
        THREADINDEX=threadindex,
        CAPTCHASERVICE=CAPTCHASERVICE,
        CAPTCHAPIKEY=CAPTCHAPIKEY,
        CAPTCHASITEKEY=CAPTCHASITEKEY,
        PHONESERVICE=PHONESERVICE,
        TOTALRETRIES=TOTALRETRIES,
        OPERATOR=OPERATOR,
        VAKAPIKEY=VAKAPIKEY,
        VAKCOUNTRY=VAKCOUNTRY,
        FIVESIMAPIKEY=FIVESIMAPIKEY,
        FIVESIMCOUNTRY=FIVESIMCOUNTRY,
        SMSHUBAPIKEY=SMSHUBAPIKEY,
        SMSHUBCOUNTRY=SMSHUBCOUNTRY,
        WEBHOOKURL=WEBHOOKURL
    )

    bypasscap = bypasscaptcha(
        CAPTCHASERVICE=CAPTCHASERVICE,
        CAPTCHAPIKEY=CAPTCHAPIKEY,
        CAPTCHASITEKEY=CAPTCHASITEKEY,
        PHONESERVICE=PHONESERVICE,
        TOTALRETRIES=TOTALRETRIES,
        OPERATOR=OPERATOR,
        VAKAPIKEY=VAKAPIKEY,
        VAKCOUNTRY=VAKCOUNTRY,
        FIVESIMAPIKEY=FIVESIMAPIKEY,
        FIVESIMCOUNTRY=FIVESIMCOUNTRY,
        SMSHUBAPIKEY=SMSHUBAPIKEY,
        SMSHUBCOUNTRY=SMSHUBCOUNTRY,
        WEBHOOKURL=WEBHOOKURL
    )

    proxyauth = loadproxyclass().loadproxy(proxytype=proxytype)[0]
    session = tls_client.Session(client_identifier="chrome_108")
    TOKENCOMBO, TOKEN, PASSWORD = gettokenclass.gettoken(totalthreads, threadindex)

    def removetoken():
        with open("files/tokens.txt", "r+") as tokenfile:
            tokenfile.seek(0)
            LINES = tokenfile.readlines()
            if TOKENCOMBO in LINES:
                LINES.remove(TOKENCOMBO)
                tokenfile.seek(0), tokenfile.truncate(), tokenfile.writelines(LINES)
            else: pass
            # else: lock.acquire(), pystyle.Write.Print(f"\t[-] Every Token from files/tokens.txt got used. File need to be refilled!\n", pystyle.Colors.red, interval=0), lock.release(), sys.exit(1)
        with open("files/failedverify.txt", "a+") as failedfile: failedfile.write(TOKENCOMBO)

    def removeinvalidtoken():
        with open("files/tokens.txt", "r+") as tokenfile:
            tokenfile.seek(0)
            LINES = tokenfile.readlines()
            if TOKENCOMBO in LINES:
                LINES.remove(TOKENCOMBO)
                tokenfile.seek(0), tokenfile.truncate(), tokenfile.writelines(LINES)
            else: pass
        with open("files/invalidtokens.txt", "a+") as invalidfile: invalidfile.write(TOKENCOMBO)

    def checktoken():
        response = session.get(url="https://discord.com/api/v9/users/@me", headers=HEADERS, proxy=proxyauth if proxytype != "" else None)

        try:
            if response.json()["message"] == "401: Unauthorized":
                removeinvalidtoken()
                pystyle.Write.Print(f"\t[-] Invalid Token: {TOKEN}!\n", pystyle.Colors.red, interval=0)
                verify(totalthreads, threadindex, proxytype)

        except KeyError:
            if "id" in response.json(): lock.acquire(), pystyle.Write.Print(f"\t[+] Valid Token {TOKEN}!\n", pystyle.Colors.green, interval=0), lock.release()
    checktoken()

    if str(PHONESERVICE).lower() == "vaksms": NUMBER, TZID = vaksms.ordernumber()
    elif str(PHONESERVICE).lower() == "fivesim": NUMBER, TZID = fivesim.ordernumber()
    elif str(PHONESERVICE).lower() == "smshub": NUMBER, TZID = smshub.ordernumber(); NUMBER = f"+{NUMBER}"

    def verifiedtoken():
        with open("files/verifiedtoken.txt", "a+") as verifiedfile: verifiedfile.write(TOKENCOMBO)
        with open("files/tokens.txt", "a+") as tokenfile:
            lines = tokenfile.readlines()
            for line in lines:
                if line.strip("\n") != TOKENCOMBO:
                    tokenfile.write(line)
            removetoken()
        lock.acquire(), pystyle.Write.Print(f"\t[+] Successfully verified {TOKEN} with {NUMBER}!\n", pystyle.Colors.green, interval=0), print(), lock.release()

        if WEBHOOKURL != "":
            webhook = DiscordWebhook(url=WEBHOOKURL, content="<@820352750344077332>", rate_limit_retry=True)
            iconurl = "https://cdn.discordapp.com/avatars/902582070335914064/a_87212f988d5e23f8edb2de2a8162744e.gif?size=1024"
            embed = DiscordEmbed(
                title='New Verified Token!',
                color='03b2f8'
                )

            embed.add_embed_field(name='Token', value=f"`{TOKEN}`", inline=False)
            embed.add_embed_field(name='Number', value=f"`{NUMBER}`", inline=False)
            embed.add_embed_field(name='SMS Code', value=f"`{VERIFYCODE}`", inline=False)
            embed.add_embed_field(name='Captcha Required', value=f"`{captcha_required}`", inline=False)
            embed.set_author(name='Infinimonster#0001', icon_url=iconurl)
            embed.set_footer(text='Discord Token Verifier', icon_url=iconurl)
            embed.set_timestamp()
            webhook.add_embed(embed)
            webhook.execute()
        verify(totalthreads, threadindex, proxytype)

    lock.acquire()
    pystyle.Write.Print(f"\t[+] Sucessfully got Number {NUMBER}\n", pystyle.Colors.green, interval=0)
    lock.release()

    data1 = {"captcha_key": None, "change_phone_reason": "user_settings_update", "phone": NUMBER}
    resp2 = session.post(
        url="https://discord.com/api/v9/users/@me/phone",
        json=data1,
        headers=HEADERS,
        proxy=proxyauth if proxytype != "" else None
    )

    if "captcha_key" in resp2.json():
        if resp2.json()["captcha_key"] == ["You need to update your app to verify your phone number."]:

            lock.acquire()
            pystyle.Write.Print("\t[*] Solving captcha... please be patient!\n", pystyle.Colors.yellow, interval=0)
            lock.release()

            CAPTCHATOKEN = False
            while CAPTCHATOKEN is False:
                CAPTCHATOKEN = bypasscap.hcaptcha()

            data1["captcha_key"] = CAPTCHATOKEN


            resp2 = session.post(
                url="https://discord.com/api/v9/users/@me/phone",
                json=data1,
                headers=HEADERS,
                proxy=proxyauth if proxytype != "" else None
            )

            captcha_required = True

    else:
        lock.acquire()
        pystyle.Write.Print("\t[*] No Captcha Solving required... Skipping!\n", pystyle.Colors.yellow, interval=0)
        lock.release()

    lock.acquire()
    if resp2.status_code == 204: pystyle.Write.Print("\t[+] Successfully requested verification code!\n", pystyle.Colors.green, interval=0)
    lock.release()

    def waitsms():
        waitcount = 0
        retries = 0
        if str(PHONESERVICE).lower() == "vaksms": waitcount, verifycode = vaksms.getcode()
        elif str(PHONESERVICE).lower() == "fivesim": waitcount, verifycode = fivesim.getcode()
        elif str(PHONESERVICE).lower() == "smshub": waitcount, verifycode = smshub.getcode()

        if waitcount == "TIMEOUT":
            retries += 1
            if retries >= TOTALRETRIES:
                pystyle.Write.Print(f"\t[-] Failed to get SMS code after {TOTALRETRIES} retries, switching token!\n", pystyle.Colors.red, interval=0)
                removetoken()

                if str(PHONESERVICE).lower() == "vaksms": vaksms.deletenumber()
                elif str(PHONESERVICE).lower() == "fivesim": fivesim.deletenumber()
                elif str(PHONESERVICE).lower() == "smshub": smshub.deletenumber()
                verify(totalthreads, threadindex, proxytype)

            else:
                pystyle.Write.Print(f"\t[-] Discord refused to send a SMS to {NUMBER}! Rerunning with another Number...\n", pystyle.Colors.red, interval=0)
                if str(PHONESERVICE).lower() == "vaksms": vaksms.deletenumber()
                elif str(PHONESERVICE).lower() == "fivesim": fivesim.deletenumber()
                elif str(PHONESERVICE).lower() == "smshub": smshub.deletenumber()
                verify(totalthreads, threadindex, proxytype)

        return verifycode
    VERIFYCODE = waitsms()

    if VERIFYCODE is not None:
        lock.acquire(), pystyle.Write.Print(f"\t[*] Found Verificationcode: {VERIFYCODE}, sending it to Discord...\n", pystyle.Colors.pink, interval=0), lock.release()
        data2 = {"phone": NUMBER, "code": VERIFYCODE}

        resp4 = session.post(
            url="https://discord.com/api/v9/phone-verifications/verify",
            json=data2,
            headers=HEADERS,
            proxy=proxyauth if proxytype != "" else None
        ).json()
        try: phone_token = resp4["token"]
        except KeyError: phone_token = None



        data3 = {"change_phone_reason": "user_settings_update", "password": PASSWORD.rstrip(), "phone_token": phone_token}
        session.post(
            url="https://discord.com/api/v9/users/@me/phone",
            json=data3,
            headers=HEADERS,
            proxy=proxyauth if proxytype != "" else None
        )

        verifiedtoken()

    elif VERIFYCODE is None:
        lock.acquire(), pystyle.Write.Print(f"\t[-] Failed to get verification code! Rerunning...\n", pystyle.Colors.red, interval=0), lock.release()
        removetoken()
        verify(totalthreads, threadindex, proxytype)

if __name__ == "__main__":
    from plugins.design import mainmenu
    from plugins.misc.init_threads import initializethreadsclass

    mainmenu.logo()
    totalthreads, proxyinput = initializethreadsclass.initthread()

    threads = []
    try:
        for threadindex in range(int(totalthreads)):
            t = threading.Thread(target=verify, args=(int(totalthreads), threadindex, proxyinput, ))
            t.start()
            threads.append(t)
            time.sleep(3)

    except ValueError:
        print(pystyle.Write.Input("\t[**] Enter a valid Thread Number!\n", pystyle.Colors.red, interval=0))
        sys.exit(1)
