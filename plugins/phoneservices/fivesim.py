import httpx as requests
import tls_client
import pystyle
import time
from plugins.configuration.load import config
from plugins.misc.get_discord_headers import getheadersclass


class fivesimverification:
    def __init__(self, **kwargs):
        self.TOTALTHREADS = kwargs.pop("TOTALTHREADS")
        self.THREADINDEX = kwargs.pop("THREADINDEX")
        self.DISCORDHEADERS = getheadersclass.getheaders(self.TOTALTHREADS, self.THREADINDEX)

        self.OPERATOR = kwargs.pop("OPERATOR")
        self.APIKEY = kwargs.pop("FIVESIMAPIKEY")
        self.COUNTRY = kwargs.pop("FIVESIMCOUNTRY")
        self.COUNTRY = self.COUNTRY.lower() if type(self.COUNTRY) is str else self.COUNTRY
        self.NUMBER = None
        self.TZID = None
        self.TIMEOUT = requests.Timeout(20.0, read=None)
        self.HEADERS = {"Authorization": f"Bearer {self.APIKEY}", "Accept": "application/json"}


    def ordernumber(self):
        url = f"https://5sim.net/v1/user/buy/activation/{self.COUNTRY}/any/discord"
        with requests.Client(headers=self.HEADERS) as client: response = client.get(url)
        if response.status_code == 400:
            pystyle.Write.Print(f"\t[*] Could not order the Number ({response.text})!\n", pystyle.Colors.yellow, interval=0)
            time.sleep(.3)
            fivesimverification.ordernumber(self)

        if response.status_code == 200:
            self.NUMBER, self.TZID = response.json()['phone'], response.json()["id"]
            return self.NUMBER, self.TZID


    def deletenumber(self):
        url = f"https://5sim.net/v1/user/cancel/{self.TZID}"
        with requests.Client(headers=self.HEADERS) as client: response = client.get(url).json()
        if response["status"] != "CANCELED": pystyle.Write.Print(f"\t[*] Could not delete the Number ({response['status']})!\n", pystyle.Colors.yellow, interval=0)

        # with requests.Client(headers=None) as client: response = client.get(url).json()
        # if response["status"] == "update":  self.DELETED = True
        # return self.DELETED


    def getcode(self):
        waitcount = 0
        session = tls_client.Session(client_identifier="safari_ios_16_0")
        url = f"https://5sim.net/v1/user/check/{self.TZID}"
        discordurl = "https://discord.com/api/v9/users/@me/phone"

        ratelimited = False
        ratelimit_duration = None
        with requests.Client(headers=self.HEADERS) as client: response = client.get(url).json()
        while response["sms"] == []:
            waitcount += 1

            pystyle.Write.Print(f"\t[*] Discord haven't sent the SMS so far... {waitcount}/120!\n", pystyle.Colors.yellow, interval=0)
            with requests.Client(timeout=self.TIMEOUT) as client:
                response = client.get(url, headers=self.HEADERS).json()
                time.sleep(.3)

                if ratelimited:
                    time.sleep(int(ratelimit_duration))

            if waitcount % 5 == 0: # run every x time to request a new sms from discord
                data = {"phone": self.NUMBER, "change_phone_reason": "user_settings_update"}

                discordresponse = session.post(
                    url=discordurl,
                    json=data,
                    headers=self.DISCORDHEADERS
                ).json()

                if "message" in discordresponse:
                    if "message" == "The resource is being rate limited.":
                        ratelimit_duration = discordresponse['retry_after']
                        pystyle.Write.Print(f"\t[-] Ratelimited for requesting a new SMS ({str(ratelimit_duration)} Seconds!) We now try to get the SMS without requesting a new one...\n", pystyle.Colors.red, interval=0)
                        ratelimited = True

            if waitcount >= 120:
                return "TIMEOUT", False

        self.VERIFYCODE = response["sms"][0]["code"] if response["status"] == "FINISHED" else None # FINISHED may need to be changed to RECEIVED if verification failed error happen after sms got delivered
        return waitcount, self.VERIFYCODE

