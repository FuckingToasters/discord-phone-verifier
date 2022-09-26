import pystyle
import os
import ctypes

# https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20
developer = "Infinimonster#0001"
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def logo():
    if os.name == "nt": ctypes.windll.kernel32.SetConsoleTitleW(f'[Mass Tools] | Ready for use <3')
    font = f"""
    \t██╗   ██╗███████╗██████╗ ██╗███████╗██╗ ██████╗ █████╗ ████████╗ ██████╗ ██████╗ 
    \t██║   ██║██╔════╝██╔══██╗██║██╔════╝██║██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
    \t██║   ██║█████╗  ██████╔╝██║█████╗  ██║██║     ███████║   ██║   ██║   ██║██████╔╝
    \t╚██╗ ██╔╝██╔══╝  ██╔══██╗██║██╔══╝  ██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗
    \t ╚████╔╝ ███████╗██║  ██║██║██║     ██║╚██████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
    \t  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
    \t                                                                            
    \t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    \tcreated by {developer}\n
    """
    clear_terminal()
    pystyle.Write.Print(font, pystyle.Colors.cyan, interval=0)
