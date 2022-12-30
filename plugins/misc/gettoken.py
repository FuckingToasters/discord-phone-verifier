import time
import sys
import pystyle


class gettokenclass:

    def gettoken(totalthreads, threadindex):
        with open("files/tokens.txt", "a+") as tokenfile:
            tokenfile.seek(0)
            LINES = tokenfile.readlines()
            TOKENCOMBO = []

            for I, TOKENCOMBO in enumerate(LINES):
                if I%totalthreads == threadindex:
                    if ":" in TOKENCOMBO: break

            if TOKENCOMBO == []: pystyle.Write.Print(f"\t[-] No more Tokens available in files/tokens.txt!\n", pystyle.Colors.red, interval=0), time.sleep(2), sys.exit(0)
            elif ":" not in TOKENCOMBO: pystyle.Write.Print("\t[*] Tokens inside files/tokens.txt are not formatted correctly (token:password)!\n", pystyle.Colors.yellow, interval=0), sys.exit(1)

            TOKEN, PASSWORD = TOKENCOMBO.split(":")
        return TOKENCOMBO, TOKEN, PASSWORD
