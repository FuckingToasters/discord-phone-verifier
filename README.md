# Discord Phone Verifier
Mass Verifing a list of discord tokens by phone.

### HOW TO INSTALL
------------------------------------
- Install Python on your System (https://python.org)
- Install the required dependencies (pip install -r requirements.txt)

### HOW TO SETUP
------------------------------------
- Create a capcha solver account & add some funds (2captcha, capmonster, anticaptcha etc.)
- Create a https://onlinesim.io account & add some funds (onlinesim is the cheapest phone provider compared to sms-activate, 5sim etc.)
- Setup files/config.json with your information (country id is the phone code eg. 49 for Germany, 7 for Russia etc.)
- Have your tokens ready in the format token:password (password is required)

### WHAT FEATURES ARE INCLUDED
------------------------------------
- ASCII Menu (Text, Color etc. can be changed in plugins/main_menu.py)
- Colored Output (Success = Green, Warning = Yellow, Error = Red & Inputs are Cyan)
- Threading (concurrent requests)
- Proxies (Avoid being ratelimited by Discord by using proxies)
- Token Checker (Before the Script starts, every token inside files/tokens.txt will be checked)
  - Invalid Tokens will be removed and added to files/invalidtokens.txt
  - Valid Tokens will stay in the same file. Phone verified Tokens will be saved inside files/verifiedtoken.txt

### FAQ - Frequently Asked Question
------------------------------------
Q: Why Accounts are being disabled after automatically adding Phone-Number?
A: This happens, if you created the Account with always the same IP or VPN / If you use the Program with same IP & VPN a lot


### Future Information
------------------------------------
If you got any Issue, please ask them here on Github.
If you want to paticipate in our Community, join our discord server: https://discord.verify.gay
