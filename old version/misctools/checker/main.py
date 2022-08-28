import httpx

FILENAME = "tokens.txt"
FORMAT = 2 # 0 = token, 1 = token:password, 2 = mail:pass:token
OUTPUT = 1 # 1 = token, 2 = token:password
with open(FILENAME, "r") as token_file: 
    token_file.seek(0)
    check_token = None
    lines = token_file.readlines()
    for token in lines:
        token = token.strip()
        
        if ":" in token:
            token = token.split(":")
            if FORMAT == 1:
                token, password = token[0], token[1]
            
            elif FORMAT == 2:
                _, password, token = token[0], token[1], token[2]
            
        headers = {"Authorization": token}
        check_token = httpx.get("https://discord.com/api/v9/users/@me", headers=headers)
        
        if check_token is None:
           print(f"No Token found inside {FILENAME}"), sys.exit(69)
        
        try:
            if check_token.json()["message"] == "401: Unauthorized":
                with open("invalid.txt", "a+") as invalid_file:
                    invalid_file.write(f"{token}\n")
                print(f"[-] Invalid Token: {token}")
                

        except KeyError:
            print(f"[+] Valid Token: {token}")
            with open("valid.txt", "a+") as valid_file:
                if OUTPUT == 1:
                    valid_file.write(f"{token}\n")
                elif OUTPUT == 2:
                    valid_file.write(f"{token}:{password}\n")