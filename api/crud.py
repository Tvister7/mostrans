from sqlalchemy.sql.expression import select
from typing import List, Optional
from psycopg2 import DataError
from api.db import get_session
from api.models import News
from datetime import datetime, timedelta


def get_news_by_date_from_db(date: int) -> List[dict]:
    session = next(get_session())
    news_from_db = session.execute(select(News.header, News.image_url, News.published_at)
                                   .order_by(News.published_at.desc())
                                   .where(News.published_at > datetime.now() - timedelta(days=date)))
    data_to_return = []
    for row in news_from_db:
        row_data = {"header": row.header,
                    "image_url": row.image_url,
                    "published_at": row.published_at.date().strftime("%Y-%m-%d")}
        data_to_return.append(row_data)
    return data_to_return


def get_last_news_title() -> str:
    session = next(get_session())
    last_title = session.execute(select(News.header).order_by(News.published_at.desc())).first()
    if last_title:
        return last_title[0]
    return "Still no news"


def add_news_to_db(data: List[dict]) -> Optional[str]:
    session = next(get_session())
    last_title = get_last_news_title()
    for news in data:
        header = news["header"]
        if header == last_title:
            return None
        image_url = news["image_url"]
        published_at = news["published_at"]
        parsed_at = news["parsed_at"]
        current_news = News(header=header,
                            image_url=image_url,
                            published_at=published_at,
                            parsed_at=parsed_at
                            )
        try:
            session.add(current_news)
        except DataError:
            session.rollback()
            return "DB insert error"
    session.commit()
