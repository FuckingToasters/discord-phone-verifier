### Important Information: 
------------------------------------
I'm working on a feature which allow you to check the account password before trying to verify the Account</br>
- Email is needed for this feature so instead of token:pass you need to put email:token:pass in tokens.txt</br>
This feature can be enabled / disabled in config.json with the next update.

 #### Why is this useful?
------------------------------------
It avoids to get sms verification code and then fail to verify account due to wrong password.

 #### Why would i want to keep it disabled?
------------------------------------
It request a second captcha solution if required.</br>
- You may want to rather waste sms than submitting an second captcha solution if the price for capsolving is higher than for ordering an SMS.</br>
- Pricing depends on captcha solving service and SMS Solving Service so you are going to decide what's better for you.


### Configuring the Verification Tool:
------------------------------------
Take a look in config.json. Here the File's content with a explaination what each line does:
```json
{
    "CAPTCHA STUFF": {
        "SERVICE": 1, # 1 = Capmonster, 2 = Anticaptcha, 3 = 2Captcha, 4 = captchaai.io, 5 = nocaptchaai.com, 6 = aio-hcaptcha
        "API KEY": "", # The Secret Key which is provided by the captcha services.
        "SITE KEY": "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34" # Key is needed to locate the captcha, it has not changed for 3 Months now but might change in the future

    },

    "PHONE STUFF": {
        "SERVICE": "SMSHUB", # select the phone service you want to use
	"OPERATOR": "mts", # enter a specific operator or 'any' if you want a random one
        "RETRIES": 5, # # Rotate current Number after x amount of retries set here with the same token (helpful if discord don't send the sms because of a flagged phonenumber)
		
        "VAKSMS": {
            "API KEY" : "", # key is needed to automatically take actions on your account (order number, delete number etc.)
            "COUNTRY" : "phillipines" # select a country for the phone verification
        },
    
        "FIVESIM": {
            "API KEY": "", # key is needed to automatically take actions on your account (order number, delete number etc.)
            "COUNTRY": "russia" # select a country for the phone verification
        },
		
	"SMSHUB": {
            "API KEY": "", # key is needed to automatically take actions on your account (order number, delete number etc.)
            "COUNTRY": 6 # you need to specify the ID for the country, find it here: https://smshub.org/en/info#getCountries
        }
    },

    "DISCORD STUFF": {
        "WEBHOOK URL": "" # Information about successful verifications can be posted to a Webhook. If you don't want to use this feature, don't enter any url
    }
}

```


### Why the SMS don't appear (sorted by Probability)
----------------------------------------------------
> Phonenumber is flagged by Discord

> Tokens or Proxies are Low Quality



### You can donate me on the crypto addresses below. 
### With every Donation i keep being motivated to update this repo & make other opensrc tools:
----------------------------------------------------
> Bitcoin: `bc1q35xnax3y9tc8kvk5hka9px8nf3wr7l0tc3emj4`

> Litecoin: `LW8amPqy5V7Ew5ofKZnFwPW8NzBM68R38y`

> Etherum: `0x05aa320E4CA3463583b9BCD6cE9b97229ae4C20A`

> Solana: `2ANHyTwPH2ggKsCp7BmtHvoRsNFHUk8hg6xsUFuHM3gu`

> Monero: `46DoyAMcKkEPhv2J2kNYKfcgb3ur7TEEbNiqSxHctTTU7ebMtLYvoU5ZsNaQFQ2JttDYZuccKKax13yZKzWq4TiUFHW6YLc`
