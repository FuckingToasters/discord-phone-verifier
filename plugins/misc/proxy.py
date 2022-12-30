import pystyle

class loadproxyclass:
    def loadproxy(self, proxytype):
        with open("files/proxies.txt", "r") as proxy_file:
            proxies = proxy_file.read().splitlines()
            proxy_split = "None"
            proxyauth, hostname, port, username, password = None, None, None, None, None

            for proxy in proxies: proxy_split = proxy.split(":")
            try:
                hostname, port, username, password = proxy_split[0], proxy_split[1], proxy_split[2], proxy_split[3]
                proxy_formatted = f"{proxytype}://{username}:{password}@{hostname}:{port}"
                if proxytype != "": proxyauth = {"all://": proxy_formatted}
                else: proxyauth = {"all://": None}

            except IndexError:
                try:
                    hostname, port, username, password = proxy_split[0], proxy_split[1], None, None
                    proxy_formatted = f"{proxytype}://{hostname}:{port}"
                    if proxytype != "": proxyauth = {"all://": proxy_formatted}
                    else: proxyauth = {"all://": None}

                except IndexError:
                    pystyle.Write.Print("\t[*] Proxies inside files/proxies.txt are not formatted correctly (IP:PORT or IP:PORT:USER:PASS)!\n", pystyle.Colors.yellow, interval=0)
                    proxyauth = {"all://": None}

            return proxyauth, hostname, port, username, password
