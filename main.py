import itertools
from auth import *
import requests as requests

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

AV_Endpoint = "https://www.alphavantage.co/query"

parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": alpha_api_key
}

response = requests.get(AV_Endpoint, params=parameters)
response.raise_for_status()
stock_data = response.json()
daily_data = stock_data["Time Series (Daily)"]
data = dict(itertools.islice(daily_data.items(), 2))
print(list(data)[0])
price_yda = float(data[list(data)[0]]["4. close"])
print(price_yda)
print(list(data)[1])
price_dby = float(data[list(data)[1]]["4. close"])
print(price_dby)

price_change = (price_yda - price_dby) / price_dby
print(price_change)

if abs(price_change) > 0.05:
    print("Get News")
