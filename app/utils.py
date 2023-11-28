import re
import feedparser
from typing import Tuple, Union
from bs4 import BeautifulSoup
from app.constants import actionable_keywords


def clean_description(description: Union[dict, list]) -> str:
    if isinstance(description, dict) and 'value' in description:
        description = description['value']

    if isinstance(description, list):
        description = ' '.join(map(str, description))

    soup: BeautifulSoup = BeautifulSoup(description, 'html.parser')
    cleaned_text: str = soup.get_text(separator=" ")
    cleaned_text: str = re.sub(r'\s+', ' ', cleaned_text)
    cleaned_text: str = cleaned_text.replace('\n', ' ').strip()

    return cleaned_text


def is_actionable(description) -> Tuple[bool, list]:
    if isinstance(description, list):
        description_texts: list = []
        for item in description:
            if isinstance(item, feedparser.FeedParserDict):
                text_content = item.get('value', '')
                description_texts.append(text_content)
            else:
                description_texts.append(str(item))
        description = ' '.join(description_texts)

    found_keywords: list = [keyword for keyword in actionable_keywords if keyword in description.lower()]
    return (True, found_keywords) if found_keywords else (False, [])

