import sys
import pystyle
import threading

class initializethreadsclass:
    def initthread():
        with open("files/tokens.txt") as tc:
            tcline = tc.readlines()
            if tcline == []: pystyle.Write.Print("\t[-] No Token found inside files/tokens.txt!\n", pystyle.Colors.red, interval=0), sys.exit(69)

        totalthreads = int(pystyle.Write.Input("\t[**] How many concurrent Threads do you want to use?: ", pystyle.Colors.cyan, interval=0))
        proxyinput = pystyle.Write.Input("\t[**] Proxy Type (http/https/socks5) | Enter nothing to use without Proxy: ", pystyle.Colors.cyan, interval=0)
        if proxyinput == "https": proxyinput = "http"

        return totalthreads, proxyinput
