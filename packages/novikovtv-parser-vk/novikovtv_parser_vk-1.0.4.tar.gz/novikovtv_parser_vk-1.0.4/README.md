# VK Parser

## Пример

```python
import os
from enum import Enum

from dotenv import load_dotenv
from pydantic import BaseModel


class ParserAPIType(int, Enum):
    """Перечисление типов парсера API."""
    Deferred = 0  # Отложенный парсинг
    Day = 1  # Дневной парсинг
    Night = 2  # Ночной парсинг


class ParserRequest(BaseModel):
    """Модель запроса на парсинг."""
    tg_user_id: int
    query: str
    type: ParserAPIType


async def main(parser_request: ParserRequest):
    load_dotenv()
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")
    max_communities = int(os.getenv("MAX_COMMUNITIES"))
    web_driver_path = os.getenv("WEB_DRIVER_PATH")
    chrome_path = os.getenv("CHROME_PATH")
    search_query = parser_request.query

    csv_text = await make_csv_text(web_driver_path, chrome_path, login, password, search_query, max_communities)

```