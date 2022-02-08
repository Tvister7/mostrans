from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class News(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    header: str
    image_url: str
    published_at: datetime
    parsed_at: datetime
