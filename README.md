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
   - find a account, which require a captcha to be solved when adding a phone-number to the account.
   - open developertools (F12)  and navigate to the Elements Tab
   - Add a Phonenumber Manually so the captcha shows up
   - use `ctrl + f` to search for the keyword `sitekey`
   - copy paste the sitekey inside the correct place in files/config.json

Q: Why the SMS Code never appears?
A: There are two different cases where this issue may apply to:
   - The Country of the Number you selected is banned from using Discord.
   - You don't use a Proxy for the Solving Service. A Proxy is required if you want to mass verify tokens.


### PSS - PHONE SERVICE SUGGESTIONS
------------------------------------
Supported Services (https://onlinesim.io, more soon)

https://vak-sms.com 
- Cheapest Service of all time. (Phillipin Number cost 1 rub which is equal to $0.017)
- I havn't tried the Numbers on Discord so far but i'll do when i'm at home. If it's good i'll implement it.

https://onlinesim.io
- Cheap Numbers for Discord on various countries cost $0.05 (Estonia & More)

https://5sim.com
- Different Users told me i should implement this Service because they have funds on it already. 
- A little bit of implementation is already made but it's not fully supported.

https://smspva.com
- Hongkong is a good Country to choose, which also cost $0.05

In case you know any other Service you want, just let me know. I might only implement a few and more for a paid version.


### FUTURE INFORMATION
------------------------------------
If you got any Issue, please ask them here on Github.
If you want to paticipate in our Community, join our discord server: https://discord.verify.gay
