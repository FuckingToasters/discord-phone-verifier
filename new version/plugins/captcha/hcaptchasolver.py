import captchatools
import json
from plugins.configuration.load import config

class bypasscaptcha():
    def __init__(self):
        self.CAPTCHASERVICE, self.CAPTCHAKEY, self.SITEKEY, _, _, _, _, _, _ = config().loadconfig()

    def hcaptcha(self):
        solver = captchatools.captcha_harvesters(solving_site=self.CAPTCHASERVICE, api_key=self.CAPTCHAKEY, captcha_type="hcaptcha", sitekey=self.SITEKEY, captcha_url="https://discord.com/api/v9/users/@me/phone")
        self.CAPTCHATOKEN = solver.get_token()
        return self.CAPTCHATOKEN
