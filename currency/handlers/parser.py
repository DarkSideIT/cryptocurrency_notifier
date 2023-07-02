from bs4 import BeautifulSoup
import requests
import time
import re

def replace_chars(text):
    pattern = re.compile('[а-яА-Я]')
    return pattern.sub(' ', text)


def get_crypto_rank(coins):
    result = {}
    html_resp = requests.get("https://coinranking.com/ru").text
    block = BeautifulSoup(html_resp, "lxml")
    rows = block.find_all("tr", class_ = "table__row--full-width")
    
    for row in rows:
        ticker = row.find("span", class_ = "profile__subtitle-name")
        if ticker:
            ticker = ticker.text.strip().lower()
            
            if ticker in coins:
                price = row.find("td", class_ = "table__cell--responsive")
                if price:
                    price = (str(price.find("div", class_ = "valuta--light").text\
                        .replace("$", "").replace(",", ".").replace(" ", "")\
                            .replace("\n", "").replace("\xa0", "")))
                    price += "$"
                    
                
                market_cap = row.find("td", class_ = "table__cell--s-hide")
                if market_cap:
                    market_cap = (str(market_cap.find("div", class_ = "valuta--light").text\
                        .replace("$", "").replace(",", ".").replace(" ", "")\
                            .replace("\n", "").replace("\xa0", "")))
                    market_cap = replace_chars(market_cap).replace(" ", "")
                    market_cap += "$ миллиардов"
                
                change = row.find("td", class_ = "table__cell--right")
                if change:
                    change = (str(change.find("div", class_ = "change--light").text\
                        .replace("\n", "").replace("\xa0", "").replace(" ", "")))
                    
                
                values = [price, market_cap, change]
                ticker = ticker.upper()
                result[ticker] = values
    
    return result
