from plugins.misc.gettoken import gettokenclass
from plugins.misc.useragent import randomagentclass
from plugins.misc.generate_superproperties import randompropertiesclass

class getheadersclass:

    @staticmethod
    def getheaders(totalthreads, threadindex):
        TOKEN = gettokenclass.gettoken(totalthreads, threadindex)[1].strip()
        USERAGENT = randomagentclass().randomagent()
        PROPERTIES = randompropertiesclass().generate_properties()
        HEADERS = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "authorization": TOKEN,
            "content-type": "application/json",
            "origin": "https://discord.com",
            "referer": "https://discord.com/channels/@me",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="108", "Google Chrome";v="108"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": USERAGENT,
            "x-debug-options": "bugReporterEnabled",
            "x-super-properties": PROPERTIES
        }
        return HEADERS
