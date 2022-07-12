import os
os.system("pip install -r requirements.txt")
os.system("cls" if os.name == "nt" else "clear")
from pystyle import Colorate, Colors

with open("tokens.txt", "r+") as rf:
    lines = rf.readlines()
  
    for line in lines:
        line = line.split(":")
      
        mail, password, tok = line[0], line[1], line[2]
        tok = tok.replace("\n", "")
        ftoken = f"{tok}:{password}\n"
      
        with open("completed.txt", "a+") as wf:
          wf.write(ftoken)
          
          colortoken = Colorate.Color(Colors.green, f"{tok}:{password}")
          colorlines = Colorate.Color(Colors.cyan, str(len(lines)))
          colorto = Colorate.Color(Colors.blue, " to")
          colorcompleted = Colorate.Color(Colors.green, " completed.txt")
          colorfile = Colorate.Color(Colors.green, " Tokens to file!")
          
        print(Colorate.Color(Colors.blue, f"Wrote {colortoken}{colorto}{colorcompleted}"))
    print(Colorate.Color(Colors.green, f"Sucessfully Wrote a total of {colorlines}{colorfile}"))
