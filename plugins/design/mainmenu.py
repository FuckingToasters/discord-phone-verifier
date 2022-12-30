import pystyle
import os
import ctypes

# https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20
developer = "Infinimonster#0002"
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def logo():
    if os.name == "nt": ctypes.windll.kernel32.SetConsoleTitleW(f'[Discord Phone Verification] | Free OpenSource Software!')
    font = f"""
    \t██╗   ██╗███████╗██████╗ ██╗███████╗██╗ ██████╗ █████╗ ████████╗ ██████╗ ██████╗
    \t██║   ██║██╔════╝██╔══██╗██║██╔════╝██║██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
    \t██║   ██║█████╗  ██████╔╝██║█████╗  ██║██║     ███████║   ██║   ██║   ██║██████╔╝
    \t╚██╗ ██╔╝██╔══╝  ██╔══██╗██║██╔══╝  ██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗
    \t ╚████╔╝ ███████╗██║  ██║██║██║     ██║╚██████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
    \t  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
    \t
    \t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    \tcreated by {developer} | https://github.com/FuckingToasters/discord-phone-verifier\n
    """
    clear_terminal()
    pystyle.Write.Print(font, pystyle.Colors.cyan, interval=0)
