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
        self.OPERATOR = config["PHONE STUFF"]["OPERATOR"]

        self.VAKAPIKEY = config["PHONE STUFF"]["VAKSMS"]["API KEY"]
        self.VAKCOUNTRY = config["PHONE STUFF"]["VAKSMS"]["COUNTRY"]
        self.FIVESIMAPIKEY = config["PHONE STUFF"]["FIVESIM"]["API KEY"]
        self.FIVESIMCOUNTRY = config["PHONE STUFF"]["FIVESIM"]["COUNTRY"]
        self.SMSHUBAPIKEY = config["PHONE STUFF"]["SMSHUB"]["API KEY"]
        self.SMSHUBCOUNTRY = config["PHONE STUFF"]["SMSHUB"]["COUNTRY"]

        # DISCORD STUFF
        self.WEBHOOKURL = config["DISCORD STUFF"]["WEBHOOK URL"]
                
        return self.CAPTCHASERVICE, \
            self.CAPTCHAPIKEY, \
            self.CAPTCHASITEKEY, \
            self.PHONESERVICE, \
            self.RETRIES, \
            self.OPERATOR, \
            self.VAKAPIKEY, \
            self.VAKCOUNTRY, \
            self.FIVESIMAPIKEY, \
            self.FIVESIMCOUNTRY, \
            self.SMSHUBAPIKEY, \
            self.SMSHUBCOUNTRY, \
            self.WEBHOOKURL
