# utils.py
import re
from datetime import date
from typing import Optional


def parse_full_name(full_name: str) -> dict:
    parts = full_name.strip().split()
    if len(parts) >= 2:
        return {
            "last_name": parts[0],
            "first_name": parts[1],
            "second_name": parts[2] if len(parts) > 2 else None,
        }
    return {}


def parse_russian_date(date_str: str) -> Optional[date]:
    if not date_str:
        return None

    months = {
        'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
        'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
        'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
    }

    cleaned = re.sub(r'[«»\"\']', '', date_str).strip()

    # Русская дата
    for ru, num in months.items():
        if ru in cleaned.lower():
            parts = cleaned.lower().replace(ru, '').split()
            day = int(parts[0]) if parts and parts[0].isdigit() else 1
            year = int(parts[-1]) if parts and parts[-1].isdigit() else 2020
            return date(year, num, day)

    # DD.MM.YYYY
    match = re.match(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', cleaned)
    if match:
        day, month, year = map(int, match.groups())
        return date(year, month, day)

    # ISO
    try:
        return date.fromisoformat(cleaned)
    except ValueError:
        return None


def extract_year(date_str: str) -> Optional[int]:
    d = parse_russian_date(date_str)
    return d.year if d else None