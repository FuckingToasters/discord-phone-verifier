import captchatools
import json
import httpx
import pystyle
import sys
import time
import pystyle
import asyncio
from plugins.configuration.load import config
from plugins.misc.proxy import loadproxyclass

_, hostname, port, username, password = loadproxyclass().loadproxy(proxytype="http")

class bypasscaptcha():
    def __init__(self, **kwargs):
        self.CAPTCHASERVICE = kwargs.pop("CAPTCHASERVICE")
        self.CAPTCHAKEY = kwargs.pop("CAPTCHAPIKEY")
        self.SITEKEY = kwargs.pop("CAPTCHASITEKEY")
        
    def hcaptcha(self):
        servicelist = [1, 2, 3, "2captcha", "anticaptcha", "capmonster"] # services which are supported by captchatools
        
        if self.CAPTCHASERVICE in servicelist:
            solver = captchatools.captcha_harvesters(solving_site=self.CAPTCHASERVICE, api_key=self.CAPTCHAKEY, captcha_type="hcaptcha", sitekey=self.SITEKEY, captcha_url="https://newassets.hcaptcha.com")
            self.CAPTCHATOKEN = solver.get_token()
            return self.CAPTCHATOKEN
            
        
        elif self.CAPTCHASERVICE == 4 or self.CAPTCHASERVICE == "captchaai.io":
            import plugins.captcha.captchaai_io as capsolver
            CAPTCHASOLUTION = asyncio.run(capsolver.Solver.solution())
            
            # from plugins.captcha.captchaai_io import solution as CAPTCHASOLUTION
            return CAPTCHASOLUTION
        
        elif self.CAPTCHASERVICE == 5 or self.CAPTCHASERVICE == "nocaptchaai.com":
            import plugins.captcha.nocaptchaai_com as capsolver
            
            CAPTCHASOLUTION = asyncio.run(capsolver.Solver.solution())
            return CAPTCHASOLUTION
        
        elif self.CAPTCHASERVICE == 6 or self.CAPTCHASERVICE == "aio-hcaptcha":
            import plugins.captcha.aiohcaptcha as capsolver
            # CAPTCHASOLUTION = asyncio.new_event_loop().run_until_complete(capsolver.Solver.solution())
            CAPTCHASOLUTION = asyncio.run(capsolver.Solver.solution())
            print(CAPTCHASOLUTION)
            return CAPTCHASOLUTION











            
