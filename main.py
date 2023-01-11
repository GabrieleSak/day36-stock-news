import itertools
import smtplib
from auth import *
import requests as requests

# STOCK = "TSLA"
STOCK = "COIN"
# COMPANY_NAME = "Tesla Inc"
COMPANY_NAME = "Coinbase"

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
price_yda = float(data[list(data)[0]]["4. close"])  # yesterday
price_dby = float(data[list(data)[1]]["4. close"])  # day before yesterday


def send_email():
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=email,
            msg=f"Subject:{COMPANY_NAME} news {STOCK}: {change_symbol}{price_change_abs_pct}% \n\n {articles}".encode(
                "utf-8")
        )


price_change = (price_yda - price_dby) / price_dby
price_change_abs_pct = abs(int(round(price_change * 100)))

articles = ""

if price_change_abs_pct > 5:
    response = requests.get(News_Endpoint, params=news_parameters)
    response.raise_for_status()
    news = response.json()
    for article in news["articles"][:3]:
        print(article["title"])
        print(article["description"])
        print("------------------------------------")
        article_tuple = ("Headline: ", article["title"], "\n", "Brief: ", article["description"], "\n\n")
        articles += "".join(article_tuple)
    if price_change > 0:
        change_symbol = u'\U0001F53A'
    else:
        change_symbol = u'\U0001F53B'
    send_email()
