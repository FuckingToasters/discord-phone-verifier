### Why there are 2 Versions (What's the difference)
------------------------------------
#### Version1:
> Support onlinesim only

> Code Design is messed up (everything in 1 file and not completed)

> Threads exit after 1 verification

> If running verify function in same Thread again, sam Token will be used

#### Version2:
> Support vaksms & 5sim only.

> Code is split in different files, making it easy to reproduce for People's who are intrested in the Code

> Threads execute the verify function in itself without using the same Token & same Number

> Higher Chance for Discord to send the SMS Code (stopped discord being lazy af)

> Webhook Support for successful verifications, making it easy to get infomrations about new verified tokens without looking in the console or the verifiedtokens.txt file

> Custom retry count in config.json in addition to the waitcount (waitcount are the ticks it'll try to get the sms which is set to 35 by default. retries is the number of times it'll try to verify the same token with another number until it switch to a next token.

> Numbers who havn't gotten the SMS in time will be delted from site (avoding discord send sms afterwards which'll use unncececary balance for a code you didn't used)

> A lot more improvments & still in development

### Note: If discord don't send the sms, try the new dev branch version: https://github.com/FuckingToasters/discord-phone-verifier/tree/dev

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
