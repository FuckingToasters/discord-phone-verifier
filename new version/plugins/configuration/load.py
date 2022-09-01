import json

class config:
    def loadconfig(self):
        with open("config.json", "r") as conf: config = json.load(conf)
        # CAPTCHA STUFF
        self.CAPTCHASERVICE = config["CAPTCHA STUFF"]["SERVICE"]
        self.CAPTCHAPIKEY = config["CAPTCHA STUFF"]["API KEY"]
        self.CAPTCHASITEKEY = config["CAPTCHA STUFF"]["SITE KEY"]

        # PHONE STUFF
        self.PHONESERVICE = config["PHONE STUFF"]["SERVICE"]
        self.RETRIES = config["PHONE STUFF"]["RETRIES"]
        self.VAKAPIKEY = config["PHONE STUFF"]["VAKSMS"]["API KEY"]
        self.VAKCOUNTRY = config["PHONE STUFF"]["VAKSMS"]["COUNTRY"]
        self.ONLINESIMAPIKEY = config["PHONE STUFF"]["ONLINESIM"]["API KEY"]
        self.ONLINESIMCOUNTRY = config["PHONE STUFF"]["ONLINESIM"]["COUNTRY"]

        # DISCORD STUFF
        self.WEBHOOKURL = config["DISCORD STUFF"]["WEBHOOK URL"]

        return self.CAPTCHASERVICE, self.CAPTCHAPIKEY, self.CAPTCHASITEKEY, self.PHONESERVICE, self.RETRIES, self.VAKAPIKEY, self.VAKCOUNTRY, self.ONLINESIMAPIKEY, self.ONLINESIMCOUNTRY, self.WEBHOOKURL
