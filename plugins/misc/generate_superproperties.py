import tls_client
import re
import os
import json
from base64 import b64encode
from plugins.misc.useragent import randomagentclass

class randompropertiesclass:
    def generate_properties(self):
        USERAGENT = randomagentclass().randomagent()
        session = tls_client.Session(client_identifier="chrome_108")
        discord = session.get(url="https://discord.com/app")
        file_with_build_num = 'https://discord.com/assets/'+re.compile(r'assets/+([a-z0-9]+)\.js').findall(discord.text)[-2]+'.js'
        bn = re.compile('\(t="[0-9]+"\)').findall(session.get(file_with_build_num).text)[0].replace("(t=\"", "").replace('")', "")
        payload = {
            "os": "Windows" if os.name == "nt" else "Linux",
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": USERAGENT,
            "browser_version": "100.0.4896.60",
            "os_version": "10",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": int(bn),
            "client_event_source": None
            }
        properties = b64encode(json.dumps(payload).encode()).decode()
        return properties
