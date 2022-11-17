import httpx as requests
import pystyle
import time
from plugins.configuration.load import config

class fivesimverification:
    def __init__(self):
        _, _, _, _, _, self.OPERATOR, _, _, self.APIKEY, self.COUNTRY, _, _, _ = config().loadconfig()
        self.COUNTRY = self.COUNTRY.lower() if self.COUNTRY is str else self.COUNTRY
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
            self.NUMBER, self.TZID = f"+{response.json()['phone']}", response.json()["id"]
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
        url = f"https://5sim.net/v1/user/check/{self.TZID}"
        discordurl = "https://discord.com/api/v9/users/@me/phone"

        with requests.Client(headers=self.HEADERS) as client: response = client.get(url).json()

        while response["sms"] == []:
            waitcount += 1

            pystyle.Write.Print(f"\t[*] Discord haven't sent the SMS so far... {waitcount}/120!\n", pystyle.Colors.yellow, interval=0)
            with requests.Client(timeout=self.TIMEOUT) as client:
                response = client.get(url, headers=self.HEADERS).json()
                time.sleep(.3)

            if waitcount >= 120:
                return "TIMEOUT", False

        print(response)
        self.VERIFYCODE = response["sms"][0]["code"] if response["status"] == "FINISHED" else None
        return waitcount, self.VERIFYCODE

