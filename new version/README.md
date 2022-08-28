### Configuring the Verification Tool:
Take a look in config.json. Here the Fil's content with a explaination what each line does:
```json
{
    "CAPTCHA STUFF": {
        "SERVICE": 2, # 1 = Capmonster, 2 = Anticaptcha, 3 = 2Captcha
        "API KEY": "", # Only with this Key the Tool can login in your Account and perform the required actions to solve the captcha
        "SITE KEY": "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34" # Don't need to be changed and is use to identify the captcha's on discord's site. The Sitekey might change at one point but it did not change for at least a month now.

    },

    "PHONE STUFF": {
        "SERVICE": "VAKSMS", # Select the Service you want to use. The best & cheapest configurations are set by default.
		
        "VAKSMS": {
            "API KEY" : "", # Same goes for the Phone Services, the APIkey is used to login into the account, order numbers, get sms, delete numbers etc.
            "COUNTRY" : "phillipines" # For vaksms phillipines is the cheapest country you can choose. a phillipines cost 1 rub which is equal to $0.017
        },
    
        "ONLINESIM": {
            "API KEY": "", # Same goes for the Phone Services, the APIkey is used to login into the account, order numbers, get sms, delete numbers etc.
            "COUNTRY": "372" # 372 is the countrycode for estonia. on Onlinesim a Estonia number cost $0.05
        }
    }
}
```


### Adding your own Phone Service (Beginner Level)
------------------------------------
- To be able to add your own Service, you need to know what APIs are and how to use them in Python.
- I made the Code easy to understand with seperating things in different files.
- The Whole main.py file include specific ifstatements which are checking for the phone service used.
- This way you can use the same variable & function names & apply the same logic within this main.py file and the files inside the phoneservices folder
- Put it inside  elif and have more phone service support.
- Here a Example: if str(PHONESERVICE).lower() == "vaksms": NUMBER, TZID = vaksms.ordernumber()
- You can change the example to elif str(PHONESERVICE).lower() == "other service" and add your own logic.
- To fully implement a own service, you need to take a look to the already supported services in the phoneservices folder, copy the file & and the new API endpoints + import it to the main file in the same way like i did in the standard supported Services.
