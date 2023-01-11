import itertools
from auth import *
import requests as requests

# STOCK = "TSLA"
STOCK = "COIN"
# COMPANY_NAME = "Tesla Inc"
COMPANY_NAME = "Coinbase"

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
News_Endpoint = "https://newsapi.org/v2/everything"

av_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "searchIn": "title, description",
    "apikey": alpha_api_key
}

news_parameters = {
    "q": COMPANY_NAME,
    "sortBy": "publishedAt",
    "apiKey": news_api_key

}

response = requests.get(AV_Endpoint, params=av_parameters)
response.raise_for_status()
stock_data = response.json()
daily_data = stock_data["Time Series (Daily)"]
data = dict(itertools.islice(daily_data.items(), 2))
price_yda = float(data[list(data)[0]]["4. close"])
price_dby = float(data[list(data)[1]]["4. close"])

price_change = (price_yda - price_dby) / price_dby

if abs(price_change) > 0.05:
    response = requests.get(News_Endpoint, params=news_parameters)
    response.raise_for_status()
    news = response.json()
    for article in news["articles"][:3]:
        print(article["title"])
        print(article["description"])
        print("------------------------------------")
