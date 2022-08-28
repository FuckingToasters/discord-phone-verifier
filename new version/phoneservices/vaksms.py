import httpx as requests
import pystyle
import json

class vakverification:
    def __init__(self):
        with open("../phoneconfig.json", "r") as conf: config = json.load(conf)
        self.APIKEY = config["VAK SMS"]["API KEY"]
        self.COUNTRY = config["VAK SMS"]["COUNTRY"]
        self.BALANCE = None
        self.STOCK = None
        self.PRICE = None
        self.NUMBER = None
        self.TZID = None
        self.VERIFYCODE = None


    def country(self):
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
        else: print(f"Country: {self.COUNTRY} is not supported.")
        return self.COUNTRY


    def getbalance(self):
        url = f"https://vak-sms.com/api/getBalance/?apiKey={self.APIKEY}"
        with requests.Client(headers=None) as client: response = client.get(url).json()

        if "error" in response:
            if response["error"] == "apiKeyNotFound": print("[-] Invalid API Key")
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
        self.NUMBER, self.TZID = response["tel"], response["idNum"]
        return self.NUMBER, self.TZID

    # send discord code here

    def waitsms(self):
        waitcount = 0
        url = f"https://vak-sms.com/api/getSmsCode/?apiKey={self.APIKEY}&idNum={self.TZID}&all"
        with requests.Client(headers=None) as client: response = client.get(url).json()
        while response["smsCode"] is None: waitcount = waitcount + 1
        if waitcount >= 30: pystyle.Write.Print(f"\t[-] Phone Number {self.NUMBER} is banned by Discord!\n", pystyle.Colors.red, interval=0)

        self.VERIFYCODE = response["smsCode"]
        pystyle.Write.Print(f"\t[*] Found Verificationcode: {self.VERIFYCODE}, sending it to Discord...\n", pystyle.Colors.yellow, interval=0)