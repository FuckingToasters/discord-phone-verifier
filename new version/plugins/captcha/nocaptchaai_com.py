# pip install asyncio requests pytest-playwright
# playwright install
# run 'python_requests_with_Playwright.py' in terminal

import datetime, requests, json, base64, asyncio, random, string, os, platform, pystyle
from playwright.async_api import async_playwright

if platform.system().startswith('Windows'): chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
elif platform.system().startswith('Linux'): chrome = "/usr/bin/chromium-browser"
else: print("Your are not using windows or linux. You need to set the chrome exe path")

class Solver:
    def __init__(self, url, sitekey, uid, apikey, headless = False, userDataPath = None):
        self.sitekey = sitekey
        self.href = url
        self.host = url.replace("https://", "").replace("http://", "")

        if "/" in self.host and not self.host.startswith("/"):
            self.host = self.host.split("/")[0]
        self.client = requests.Session()
        self.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.141 Whale/3.15.136.29 Safari/537.36"
        self.nocaptchaai = {
            "uid": uid,
            "apikey": apikey,
            "solver": "https://free.nocaptchaai.com/api/solve"
        }
        self.version = self.client.get("https://hcaptcha.com/1/api.js?render=explicit&onload=hcaptchaOnLoad", headers={
            "user-agent": self.userAgent,
            "referer": self.host,
            "accept-language": "en-US,en;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept": "*/*",
            "sec-fetch-dest": "script",
            "sec-ch-ua-platform": "\"Windows\""
        }).text.split("assetUrl")[1].split("https://newassets.hcaptcha.com/captcha/v1/")[1].split("/static")[0]
        self.headless = headless
        self.userDataPath = userDataPath
        if self.userDataPath == None: self.userDataPath = os.path.join(os.getcwd(), "browserUserData\\")
        if not os.path.exists(self.userDataPath):
            os.mkdir(self.userDataPath)

    async def _getHsw(self, m, c):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.add_script_tag(url="https://newassets.hcaptcha.com/c/b0c89e7a/hsw.js")
                response = await page.evaluate(f"hsw(\"{c}\")")
                await page.close()
                await browser.close()
                return str(response)
        except:
            print("Chrome executablePath not correct. please set the correct chrome/chromium path")
            
    async def _getCaptcha(self):
        o = json.loads(self.client.post(f"https://hcaptcha.com/checksiteconfig?v={self.version}&host={self.host}&sitekey={self.sitekey}&sc=1&swa=1", headers={
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "text/plain",
            "origin": "https://newassets.hcaptcha.com",
            "referer": "https://newassets.hcaptcha.com/",
            "user-agent": self.userAgent,
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site"
        }).text)
        l = json.loads(base64.b64decode(str((o["c"]["req"].split(".")[1]) + ("=" * 8)).encode()).decode())["l"]
        self.s = self.client.get(f"{l}/hsw.js", headers={
            "user-agent": self.userAgent,
            "referer": f"https://newassets.hcaptcha.com/captcha/v1/{self.version}/static/hcaptcha.html",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "accept": "*/*"
        }).text
        h = await self._getHsw(self.s, o["c"]["req"])
        w = "".join(random.choice(string.ascii_lowercase) for i in range(12))
        p = {
            "v": self.version,
            "sitekey": self.sitekey,
            "host": self.host,
            "hl": "en",
            "motionData": "{\"st\":1661663397717,\"mm\":[[2,19,1661663398690],[19,24,1661663398706],[31,26,1661663398722],[39,29,1661663398745],[40,28,1661663398833]],\"mm-mp\":17.875,\"md\":[[40,28,1661663399130]],\"md-mp\":0,\"mu\":[[40,28,1661663399201]],\"mu-mp\":0,\"v\":1,\"topLevel\":{\"inv\":false,\"st\":1661663397460,\"sc\":{\"availWidth\":1920,\"availHeight\":1032,\"width\":1920,\"height\":1080,\"colorDepth\":24,\"pixelDepth\":24,\"availLeft\":0,\"availTop\":0,\"onchange\":null,\"isExtended\":false},\"nv\":{\"vendorSub\":\"\",\"productSub\":\"20030107\",\"vendor\":\"NAVER Corp.\",\"maxTouchPoints\":0,\"scheduling\":{},\"userActivation\":{},\"doNotTrack\":null,\"geolocation\":{},\"connection\":{},\"pdfViewerEnabled\":true,\"webkitTemporaryStorage\":{},\"webkitPersistentStorage\":{},\"hardwareConcurrency\":4,\"cookieEnabled\":true,\"appCodeName\":\"Mozilla\",\"appName\":\"Netscape\",\"appVersion\":\"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.87 Whale/3.16.138.22 Safari/537.36\",\"platform\":\"Win32\",\"product\":\"Gecko\",\"userAgent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.87 Whale/3.16.138.22 Safari/537.36\",\"language\":\"en-US\",\"languages\":[\"en-US\"],\"onLine\":true,\"webdriver\":false,\"bluetooth\":{},\"clipboard\":{},\"credentials\":{},\"keyboard\":{},\"managed\":{},\"mediaDevices\":{},\"storage\":{},\"serviceWorker\":{},\"wakeLock\":{},\"deviceMemory\":8,\"ink\":{},\"hid\":{},\"locks\":{},\"mediaCapabilities\":{},\"mediaSession\":{},\"permissions\":{},\"presentation\":{},\"serial\":{},\"virtualKeyboard\":{},\"usb\":{},\"xr\":{},\"userAgentData\":{\"brands\":[{\"brand\":\"Whale\",\"version\":\"3\"},{\"brand\":\" Not;A Brand\",\"version\":\"99\"},{\"brand\":\"Chromium\",\"version\":\"104\"}],\"mobile\":false,\"platform\":\"Windows\"},\"plugins\":[\"internal-pdf-viewer\",\"internal-pdf-viewer\",\"internal-pdf-viewer\",\"internal-pdf-viewer\",\"internal-pdf-viewer\"]},\"dr\":\"\",\"exec\":false,\"wn\":[[1186,964,1,1661663397465]],\"wn-mp\":0,\"xy\":[[0,0,1,1661663397478]],\"xy-mp\":0,\"mm\":[[952,0,1661663398099],[912,0,1661663398121],[890,2,1661663398137],[868,7,1661663398154],[826,20,1661663398177],[794,29,1661663398193],[760,39,1661663398213],[713,53,1661663398234],[225,279,1661663398621],[239,291,1661663398641],[250,297,1661663398657],[264,304,1661663398673]],\"mm-mp\":22.384615384615383},\"session\":[],\"widgetList\":[\"" + w + "\"],\"widgetId\":\"" + w + "\",\"href\":\"" + self.href + "\",\"prev\":{\"escaped\":false,\"passed\":false,\"expiredChallenge\":false,\"expiredResponse\":false}}".replace("1661663", str(round(datetime.datetime.now().timestamp()))[:7]),
            "n": h,
            "c": "{\"type\":\"" + o["c"]["type"] + "\",\"req\":\"" + o["c"]["req"] + "\"}"
        }
        c = self.client.post(f"https://hcaptcha.com/getcaptcha/{self.sitekey}", headers={
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-length": str(len(p)),   
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://newassets.hcaptcha.com",
            "referer": "https://newassets.hcaptcha.com/",
            "user-agent": self.userAgent,
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site"
        }, data=p).json()
        return c

    async def solveCaptcha(self):
        headers = {
            "Authority": "hcaptcha.com",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://newassets.hcaptcha.com/",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "User-Agent": self.userAgent,
        }

        c = await self._getCaptcha(); k, t = c["key"], c["tasklist"]; i, t_, z = {}, {}, 0
        for u in t:
            img_base64 = base64.b64encode(requests.get(str(u["datapoint_uri"]), headers = headers).content)
            img_base64_decoded = img_base64.decode('utf-8') 
            url, task_key =img_base64_decoded , str(u["task_key"])
            i[z], t_[url] = url, task_key
            z += 1
        g = c["requester_question"]["en"]
        pystyle.Write.Print(f"\t[+] Successfully got captcha {g}; Solving...\n", pystyle.Colors.pink, interval=0)

        task_result = requests.post(self.nocaptchaai["solver"], json={
            "images": i,
            "target": g,
            "method": "hcaptcha_base64",
            "site": self.href,
            "sitekey": self.sitekey
        }, headers={
            "Content-type": "application/json",
            "uid": self.nocaptchaai["uid"],
            "apikey": self.nocaptchaai["apikey"]
        }).json()

        status = 'new'
        if task_result['status'] == 'new':
            url, p2, z, answer = task_result["url"], None, 0, {}
            await asyncio.sleep(2.5)
            while True:
                p2 = requests.get(url).text
                if "solved" in p2: p2 = json.loads(p2); status = 'solved'; break
                elif not "queue" in p2: return False
                if z >= 5: print(p2); return False
                z += 1
                await asyncio.sleep(5.0)
                
            for d in i:
                if str(d) in p2["solution"]: answer[t_[i[d]]] = "true"
                else: answer[t_[i[d]]] = "false"

        elif task_result['status'] == 'solved':
            answer = {}
            status = 'solved'
            for d in i:
                if d in task_result["solution"]: answer[t_[i[d]]] = "true"
                else: answer[t_[i[d]]] = "false"

        # print(answer)
        if status == 'solved':
            h = await self._getHsw(self.s, c["c"]["req"])
            s = {
                "v": self.version,
                "job_mode": "image_label_binary",
                "answers": answer,
                "serverdomain": self.host,
                "sitekey": self.sitekey,
                "motionData": "{\"st\":1661664971836,\"dct\":1661664971836,\"mm\":[[222,303,1661664984346],[232,305,1661664984370],[245,306,1661664984386],[263,308,1661664984402],[286,308,1661664984418],[312,308,1661664984434],[336,308,1661664984450],[360,309,1661664984474],[362,309,1661664984490],[363,310,1661664984586],[361,312,1661664984626],[360,315,1661664984642],[359,324,1661664984658],[356,340,1661664984674],[351,367,1661664984690],[346,396,1661664984706],[340,435,1661664984730],[336,462,1661664984753],[336,469,1661664984769],[335,474,1661664984785],[334,475,1661664984890],[330,475,1661664984922],[313,459,1661664984945],[290,433,1661664984962],[259,401,1661664984978],[214,361,1661664984994],[165,323,1661664985010],[100,276,1661664985034],[71,256,1661664985050],[54,242,1661664985066],[47,237,1661664985082],[46,234,1661664985098],[45,233,1661664985114],[46,233,1661664985266],[51,233,1661664985282],[73,231,1661664985298],[112,225,1661664985314],[167,217,1661664985330],[262,203,1661664985354],[319,190,1661664985370],[364,176,1661664985386],[387,172,1661664985402],[388,172,1661664985562],[384,175,1661664985578],[378,180,1661664985594],[367,188,1661664985610],[351,197,1661664985626],[331,213,1661664985642],[295,240,1661664985665],[270,261,1661664985682],[238,291,1661664985706],[222,306,1661664985722],[210,316,1661664985746],[208,319,1661664986050],[202,321,1661664986066],[192,328,1661664986082],[177,335,1661664986098],[158,348,1661664986114],[135,363,1661664986130],[109,381,1661664986146],[81,400,1661664986162],[44,426,1661664986186],[25,439,1661664986202],[11,449,1661664986226],[13,450,1661664986442],[40,450,1661664986458],[83,451,1661664986474],[169,453,1661664986498],[216,459,1661664986514],[246,460,1661664986530],[266,464,1661664986546],[272,465,1661664986562],[276,462,1661664986746],[279,439,1661664986770],[283,406,1661664986786],[288,362,1661664986802],[293,301,1661664986825],[296,265,1661664986842],[299,222,1661664986866],[304,197,1661664986890],[304,189,1661664986906],[304,187,1661664986922],[303,186,1661664987018],[274,180,1661664987042],[233,175,1661664987058],[188,168,1661664987074],[143,163,1661664987090],[105,161,1661664987106],[75,157,1661664987122],[57,155,1661664987146],[56,155,1661664987162],[55,155,1661664987186],[54,155,1661664987210],[53,156,1661664987458],[53,157,1661664987498],[53,159,1661664987514],[53,162,1661664987530],[53,168,1661664987554],[54,176,1661664987570],[56,184,1661664987586],[58,200,1661664987602],[62,225,1661664987618],[67,259,1661664987634],[73,301,1661664987650],[83,376,1661664987674],[91,421,1661664987690],[94,450,1661664987706],[97,465,1661664987722],[98,473,1661664987834],[100,472,1661664987890],[109,468,1661664987906],[136,460,1661664987930],[163,453,1661664987946],[194,446,1661664987962],[227,437,1661664987978],[256,431,1661664987994],[279,425,1661664988010],[295,422,1661664988026],[303,421,1661664988042],[308,419,1661664988066],[308,420,1661664988386],[309,425,1661664988402],[311,430,1661664988418],[312,437,1661664988434],[316,450,1661664988458],[318,462,1661664988474],[322,472,1661664988490],[325,483,1661664988513],[327,485,1661664988529],[327,488,1661664988545],[324,490,1661664988794],[302,475,1661664988810],[269,450,1661664988826],[208,405,1661664988850],[163,371,1661664988866],[120,335,1661664988882],[85,305,1661664988898],[62,282,1661664988914],[52,270,1661664988930],[50,267,1661664988962],[50,264,1661664989122],[52,251,1661664989138],[53,235,1661664989154],[57,213,1661664989170],[59,196,1661664989186],[61,183,1661664989202],[63,171,1661664989218],[63,166,1661664989234],[64,163,1661664989258],[65,163,1661664989370],[68,165,1661664989394],[81,171,1661664989410],[106,181,1661664989426],[142,198,1661664989442],[188,216,1661664989458],[233,236,1661664989474],[269,256,1661664989490],[296,271,1661664989506],[307,280,1661664989522],[308,281,1661664989562],[308,282,1661664989642],[308,283,1661664989658],[306,294,1661664989682],[306,317,1661664989706],[306,339,1661664989722],[306,363,1661664989738],[306,385,1661664989754],[309,401,1661664989770],[312,417,1661664989786],[316,430,1661664989802],[318,437,1661664989818],[319,440,1661664989834],[319,443,1661664989850],[320,444,1661664989874],[321,445,1661664989906],[319,445,1661664990018],[310,445,1661664990034],[291,445,1661664990050],[264,445,1661664990066],[229,445,1661664990082],[176,445,1661664990106],[135,445,1661664990130],[123,445,1661664990298],[132,445,1661664990314],[147,443,1661664990330],[189,436,1661664990354],[236,425,1661664990370],[287,411,1661664990386],[363,393,1661664990410],[397,391,1661664990426],[395,388,1661664990602],[388,385,1661664990618],[379,378,1661664990634],[369,367,1661664990650],[360,351,1661664990666],[349,328,1661664990682],[338,302,1661664990698],[326,273,1661664990714],[318,248,1661664990730],[314,228,1661664990746],[311,211,1661664990762],[310,199,1661664990778],[310,193,1661664990794],[310,189,1661664990818],[310,190,1661664990930],[310,220,1661664990954],[310,253,1661664990970],[310,298,1661664990986],[310,346,1661664991002],[313,390,1661664991018],[316,436,1661664991041],[318,454,1661664991058],[318,465,1661664991074],[319,470,1661664991090],[319,473,1661664991106],[319,474,1661664991138],[318,475,1661664991178],[314,475,1661664991194],[301,475,1661664991210],[280,475,1661664991226],[250,470,1661664991242],[212,465,1661664991258],[156,456,1661664991281],[126,451,1661664991298],[111,448,1661664991314],[106,447,1661664991330],[107,447,1661664991490],[112,447,1661664991514],[123,448,1661664991530],[140,448,1661664991546],[161,448,1661664991562],[199,445,1661664991585],[227,441,1661664991601],[253,437,1661664991618],[275,437,1661664991634],[291,436,1661664991650],[306,436,1661664991673],[308,436,1661664991689],[311,437,1661664991834],[312,440,1661664991850],[314,449,1661664991873],[317,457,1661664991890],[319,465,1661664991906],[322,473,1661664991929],[323,475,1661664991945],[323,477,1661664991970],[321,478,1661664992138],[304,473,1661664992154],[273,461,1661664992170],[236,444,1661664992186],[177,410,1661664992210],[138,385,1661664992226],[102,357,1661664992242],[74,336,1661664992258],[53,320,1661664992274],[43,312,1661664992290],[42,311,1661664992426],[44,313,1661664992442],[47,318,1661664992458],[52,327,1661664992474],[67,353,1661664992498],[81,378,1661664992514],[98,404,1661664992530],[116,429,1661664992546],[132,448,1661664992562],[149,461,1661664992578],[171,471,1661664992601],[179,475,1661664992618],[183,476,1661664992634],[185,478,1661664992650],[186,479,1661664992810],[187,479,1661664992826],[193,484,1661664992850],[196,484,1661664992866],[202,482,1661664992882],[211,476,1661664992898],[220,471,1661664992914],[236,457,1661664992938],[244,451,1661664992954],[249,446,1661664992970],[253,441,1661664992986],[254,438,1661664993002],[256,436,1661664993018],[254,438,1661664993146],[230,441,1661664993170],[194,445,1661664993194],[151,450,1661664993218],[125,454,1661664993234],[104,458,1661664993258],[100,458,1661664993282],[105,454,1661664993546],[127,426,1661664993570],[146,397,1661664993586],[159,369,1661664993602],[173,336,1661664993618],[186,313,1661664993634],[192,293,1661664993650],[197,275,1661664993666],[202,264,1661664993682],[203,258,1661664993698],[204,256,1661664993810],[205,256,1661664993826],[210,256,1661664993842],[222,261,1661664993858],[246,268,1661664993874],[271,273,1661664993890],[295,279,1661664993906],[315,283,1661664993929],[315,285,1661664994026],[314,287,1661664994042],[311,295,1661664994058],[303,315,1661664994081],[295,333,1661664994098],[290,347,1661664994114],[285,363,1661664994130],[283,372,1661664994146],[281,378,1661664994162],[281,382,1661664994178],[280,385,1661664994202],[279,386,1661664994266],[276,386,1661664994322],[271,386,1661664994338],[254,375,1661664994362],[237,362,1661664994378],[210,344,1661664994401],[196,335,1661664994418],[184,326,1661664994434],[180,323,1661664994450],[179,323,1661664994570],[179,324,1661664994618],[179,328,1661664994634],[179,337,1661664994650],[179,348,1661664994666],[179,360,1661664994682],[176,374,1661664994698],[168,386,1661664994714],[160,398,1661664994730],[143,417,1661664994753],[132,426,1661664994770],[120,435,1661664994786],[111,441,1661664994802],[106,444,1661664994818],[103,446,1661664994866],[105,446,1661664995010],[120,446,1661664995026],[146,446,1661664995042],[178,446,1661664995058],[227,446,1661664995081],[254,446,1661664995098],[272,446,1661664995114],[281,446,1661664995130],[283,446,1661664995154],[284,448,1661664995338],[284,453,1661664995354],[281,460,1661664995370],[276,469,1661664995386],[267,476,1661664995402],[254,481,1661664995418],[238,484,1661664995434],[216,485,1661664995450],[191,485,1661664995466],[160,485,1661664995489],[149,485,1661664995506],[145,484,1661664995674],[145,474,1661664995690],[145,453,1661664995706],[139,425,1661664995722],[124,380,1661664995738],[93,306,1661664995762],[70,261,1661664995778],[51,226,1661664995794],[39,207,1661664995810],[34,195,1661664995826],[33,192,1661664995850],[33,194,1661664995930],[37,202,1661664995946],[55,218,1661664995962],[90,239,1661664995978],[163,266,1661664996002],[233,280,1661664996026],[264,284,1661664996042],[278,286,1661664996058],[279,287,1661664996225],[279,289,1661664996242],[278,297,1661664996258],[275,310,1661664996274],[274,325,1661664996290],[273,346,1661664996306],[269,367,1661664996322],[266,386,1661664996338],[264,403,1661664996354],[263,412,1661664996370],[263,415,1661664996386],[261,419,1661664996410],[261,421,1661664996434],[260,423,1661664996514],[259,424,1661664996530],[257,424,1661664996546],[243,404,1661664996569],[224,372,1661664996585],[196,334,1661664996602],[168,297,1661664996618],[140,265,1661664996634],[116,239,1661664996650],[98,221,1661664996666],[89,211,1661664996682],[81,205,1661664996698],[76,197,1661664996714],[71,192,1661664996730],[66,188,1661664996754],[65,187,1661664996786],[66,188,1661664996906],[69,193,1661664996922],[81,204,1661664996938],[102,217,1661664996954],[133,232,1661664996970],[172,251,1661664996986],[216,269,1661664997002],[281,295,1661664997026],[317,308,1661664997042],[348,321,1661664997065],[352,324,1661664997081],[350,328,1661664997202],[348,343,1661664997218],[344,364,1661664997234],[341,388,1661664997250],[333,410,1661664997266],[325,429,1661664997282],[320,442,1661664997298],[316,450,1661664997314],[314,454,1661664997330],[313,456,1661664997346],[312,458,1661664997362],[310,460,1661664997386],[308,461,1661664997410],[307,461,1661664997426],[301,463,1661664997450],[290,463,1661664997466],[270,463,1661664997482],[243,463,1661664997498],[194,463,1661664997522],[160,463,1661664997538],[131,463,1661664997554],[110,463,1661664997570],[99,463,1661664997586],[97,465,1661664997914],[103,469,1661664997930],[119,474,1661664997946],[144,481,1661664997962],[173,490,1661664997978],[206,500,1661664997994],[239,510,1661664998010],[272,521,1661664998026],[303,530,1661664998050],[310,533,1661664998066],[312,533,1661664998114],[313,534,1661664998146],[315,534,1661664998178],[318,538,1661664998202],[322,544,1661664998226],[324,547,1661664998242],[328,551,1661664998266],[331,554,1661664998290],[333,556,1661664998314],[335,558,1661664998330],[336,558,1661664998346],[341,559,1661664998370],[342,559,1661664998394],[343,560,1661664998410],[343,560,1661664999193]],\"mm-mp\":18.977353149327644,\"md\":[[209,317,1661664985946],[54,155,1661664987346],[323,477,1661664991986],[100,458,1661664993426],[103,446,1661664994874],[65,187,1661664996802],[343,560,1661664999187]],\"md-mp\":927.1481481481482,\"mu\":[[209,317,1661664986025],[54,155,1661664987442],[323,477,1661664992081],[100,458,1661664993498],[103,446,1661664994937],[65,187,1661664996858],[343,560,1661664999265]],\"mu-mp\":927.6666666666666,\"topLevel\":{\"inv\":false,\"st\":1661663397460,\"sc\":{\"availWidth\":1920,\"availHeight\":1032,\"width\":1920,\"height\":1080,\"colorDepth\":24,\"pixelDepth\":24,\"availLeft\":0,\"availTop\":0,\"onchange\":null,\"isExtended\":false},\"nv\":{\"vendorSub\":\"\",\"productSub\":\"20030107\",\"vendor\":\"NAVER Corp.\",\"maxTouchPoints\":0,\"scheduling\":{},\"userActivation\":{},\"doNotTrack\":null,\"geolocation\":{},\"connection\":{},\"pdfViewerEnabled\":true,\"webkitTemporaryStorage\":{},\"webkitPersistentStorage\":{},\"hardwareConcurrency\":4,\"cookieEnabled\":true,\"appCodeName\":\"Mozilla\",\"appName\":\"Netscape\",\"appVersion\":\"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.87 Whale/3.16.138.22 Safari/537.36\",\"platform\":\"Win32\",\"product\":\"Gecko\",\"userAgent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.87 Whale/3.16.138.22 Safari/537.36\",\"language\":\"en-US\",\"languages\":[\"en-US\"],\"onLine\":true,\"webdriver\":false,\"bluetooth\":{},\"clipboard\":{},\"credentials\":{},\"keyboard\":{},\"managed\":{},\"mediaDevices\":{},\"storage\":{},\"serviceWorker\":{},\"wakeLock\":{},\"deviceMemory\":8,\"ink\":{},\"hid\":{},\"locks\":{},\"mediaCapabilities\":{},\"mediaSession\":{},\"permissions\":{},\"presentation\":{},\"serial\":{},\"virtualKeyboard\":{},\"usb\":{},\"xr\":{},\"userAgentData\":{\"brands\":[{\"brand\":\"Whale\",\"version\":\"3\"},{\"brand\":\" Not;A Brand\",\"version\":\"99\"},{\"brand\":\"Chromium\",\"version\":\"104\"}],\"mobile\":false,\"platform\":\"Windows\"},\"plugins\":[\"internal-pdf-viewer\",\"internal-pdf-viewer\",\"internal-pdf-viewer\",\"internal-pdf-viewer\",\"internal-pdf-viewer\"]},\"dr\":\"\",\"exec\":false,\"wn\":[],\"wn-mp\":0,\"xy\":[],\"xy-mp\":0,\"mm\":[[741,425,1661664990434],[744,424,1661664990578]],\"mm-mp\":160.35668789808918,\"lpt\":1661663520202,\"md\":[],\"md-mp\":0,\"mu\":[],\"mu-mp\":0},\"v\":1}",
                "n": h,
                "c": "{\"type\":\"" + c["c"]["type"] + "\",\"req\":\"" + c["c"]["req"] + "\"}"
            }; s["motionData"] = s["motionData"].replace("1661664", str(round(datetime.datetime.now().timestamp()))[:7])
            
            checkcaptcha = self.client.post(f"https://hcaptcha.com/checkcaptcha/{self.sitekey}/{k}", json=s, headers={
                "Authority": "hcaptcha.com",
                "content-type": "application/json",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "content-length": str(len(s)),
                "accept": "*/*",
                "origin": "https://newassets.hcaptcha.com",
                "referer": "https://newassets.hcaptcha.com/",
                "user-agent": self.userAgent,
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site"
            })
            # print(checkcaptcha.json())
            if "generated_pass_UUID" in checkcaptcha.json():
                return checkcaptcha.json()["generated_pass_UUID"]

            else:
                return False
        else: return "Something wrong"

    async def solution():
        from plugins.configuration.load import config
        _, CAPTCHAKEY, SITEKEY, _, _, _, _, _, _, _, _, _, _ = config().loadconfig()
        UID = "infinimonster"
        SITE = "https://discord.com/api/v9/users/@me/phone"

        """
        if UID == "" or self.CAPTCHAKEY == "" or SITE == "" or self.SITEKEY == "":
            print("You need to set uid apikey site and sitekey first.")
            return False
        """

        config = {
            "solver": {
                "uid": UID,
                "apikey": CAPTCHAKEY
            },
            "hcaptcha": {
                "url": SITE,
                "sitekey": SITEKEY
            },
            "headless": True # browser visibility
        }

        solver = Solver(config["hcaptcha"]["url"], config["hcaptcha"]["sitekey"], config["solver"]["uid"], config["solver"]["apikey"], config["headless"])
        result = await solver.solveCaptcha()

        if result is False:
            pystyle.Write.Print(f"\t[+] Couldn't solve Captcha; retrying...\n", pystyle.Colors.yellow, interval=0)
            await Solver.solution()
        
        result = str(result)
        return result
        # input()

"""
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
"""
