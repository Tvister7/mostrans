import time

import requests
from bs4 import BeautifulSoup
import locale
from datetime import datetime, timezone
from typing import List

from api.crud import add_news_to_db
from api.db import init_db

location = locale.setlocale(locale.LC_TIME, ('ru_RU', 'UTF-8'))
URL = "https://mosmetro.ru/news/"
init_db()


def parse_news() -> List[dict]:
    current_year = datetime.now(timezone.utc).year

    page = requests.get(URL)

    soup = BeautifulSoup(page.text, "html.parser")

    all_news = set(soup.findAll("a", class_="news-card"))

    all_hidden_news = set(soup.findAll("a", class_="news-card hidden"))

    unique_news = all_news - all_hidden_news

    data_to_db = []

    for news in unique_news:
        header = news.find("div", class_="news-card__caption").string
        image_url = news.find("div", class_="news-card__image").get('style')[22:-1]
        published_at = news.find("div", class_="news-card__date").string
        time_to_db = datetime.strptime(str(current_year) + published_at, "%Y%d %B, %H:%M")
        data_to_db.append({"header": header,
                           "image_url": image_url,
                           "published_at": time_to_db,
                           "parsed_at": datetime.now()
                           })

    return data_to_db


if __name__ == "__main__":
    while True:
        data = parse_news()
        error = add_news_to_db(data)
        if not error:
            time.sleep(600)
        else:
            break

    print("Parsing is over!")

