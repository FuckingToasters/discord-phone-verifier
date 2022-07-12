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
  - Valid Tokens will stay in the same file. 
  - Phone verified Tokens will be saved inside files/verifiedtoken.txt and removed from files/tokens.txt

### FAQ - FREQUENTLY ASKED QUESTION
------------------------------------
Q: Why Accounts are being disabled after automatically adding Phone-Number?
A: It happens,
   - If you created the Account with always the same IP or VPN
   - If you use the Program with same IP & VPN
   - If you use bad proxies / bad VPN

Q: Why i get a invalid sitekey error?
A: You need to get a new sitekey by following the steps below:
   - find a account, which require a captcha to be solved when joining servers or make one.
   - open developertools (F12)  and navigate to the Elements Tab
   - Prentent to join a server so the captcha shows up
   - use `ctrl + f` to search for the keyword `sitekey`
   - copy paste the sitekey inside the correct place in files/config.json

### PSS - Phone Service Suggestions
------------------------------------
Supported Services (https://onlinesim.io, more soon)
Depending on the Service you use, different countries have different prices.
https://sms-activate.ru & https://5sim.com are the most expencive ones out there and are not recommended by me.
On https://onlinesim.io the cheapest numbers for discord on various countries cost $0.05 (Estonia & More)
On https://smspva.com Hongkong is a good Country to choose, which also cost $0.05


### FUTURE INFORMATION
------------------------------------
If you got any Issue, please ask them here on Github.
If you want to paticipate in our Community, join our discord server: https://discord.verify.gay
