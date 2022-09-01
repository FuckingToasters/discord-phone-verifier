import httpx as requests
import pystyle
import threading
import sys
from plugins.configuration.load import config

class vakverification:
    def __init__(self):
        _, _, _, _, _, self.APIKEY, self.COUNTRY, _, _ = config().loadconfig()
        self.BALANCE = None
        self.STOCK = None
        self.PRICE = None
        self.NUMBER = None
        self.TZID = None
        self.VERIFYCODE = None
        self.BANNED = False
        self.DELETED = False

        def country(self):
            lock = threading.Lock()
            cl = {
                "Denmark": "dk",
                "Estonia": "ee",
                "Finland": "fi",
                "France": "fr",
                "Germany": "de",
                "Hong Kong": "hk",
                "Indonesia": "id",
                "Kazakhstan": "kz",
                "Latvia": "lv",
                "Lithuania": "lt",
                "Mexico": "mx",
                "Netherlands": "nl",
                "Phillipines": "ph",
                "Poland": "pl",
                "Portugal": "pt",
                "Romania": "ro",
                "Russia": "ru",
                "Spain": "es",
                "Sweden": "se",
                "Ukraine": "ua",
                "United Kingdom": "gb",
                "Vietnam": "vn"
            }
            if self.COUNTRY.title() in cl: self.COUNTRY = cl[self.COUNTRY.title()]
            else: lock.acquire(), pystyle.Write.Print(f"\tCountry: {self.COUNTRY} is not supported.!\n", pystyle.Colors.red, interval=0), lock.release()
            return self.COUNTRY
        self.COUNTRY = country(self)


    def getbalance(self):
        lock = threading.Lock()
        url = f"https://vak-sms.com/api/getBalance/?apiKey={self.APIKEY}"
        with requests.Client(headers=None) as client: response = client.get(url).json()

        if "error" in response:
            if response["error"] == "apiKeyNotFound": lock.acquire(), pystyle.Write.Print(f"\t[-] Invalid API Key!\n", pystyle.Colors.red, interval=0), lock.release()
        else: self.BALANCE = response['balance']
        return self.BALANCE


    def getnumberandpricecount(self):
        url = f"https://vak-sms.com/api/getCountNumber/?apiKey={self.APIKEY}&service=dc&country={self.COUNTRY}&price"
        with requests.Client(headers=None) as client: response = client.get(url).json()
        self.STOCK, self.PRICE = response['dc'], response['price']
        return self.STOCK, self.PRICE


    def ordernumber(self):
        url = f"https://vak-sms.com/api/getNumber/?apiKey={self.APIKEY}&service=dc&country={self.COUNTRY}"
        with requests.Client(headers=None) as client: response = client.get(url).json()
        self.NUMBER, self.TZID = str(response["tel"]), response["idNum"]
        self.NUMBER = f"+{self.NUMBER}"
        return self.NUMBER, self.TZID
    
    def deletenumber(self):
        url = f"https://vak-sms.com/api/setStatus/?apiKey={self.APIKEY}&status=end&idNum={self.TZID}"
        response = requests.get(url).json()
        if response["status"] != "update": pystyle.Write.Print(f"\t[*] Could not delete the Number ({response['status']})!\n", pystyle.Colors.yellow, interval=0)

        # with requests.Client(headers=None) as client: response = client.get(url).json()
        # if response["status"] == "update":  self.DELETED = True
        # return self.DELETED
