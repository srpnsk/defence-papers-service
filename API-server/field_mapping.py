import re
from typing import Any, Dict, Optional

# Вспомогательные функции
def get_thesis_id(ctx): return ctx["thesis_id"]
def get_applicant_id(ctx): return ctx["applicant_id"]
def get_supervisor_id(ctx): return ctx.get("supervisor_id")
def get_council_id(ctx): return ctx["council_id"]
def get_chairman_id(ctx): return ctx["chairman_id"]
def get_secretary_id(ctx): return ctx["secretary_id"]
def get_specialty_id(ctx): return ctx["specialty_id"]

def parse_russian_date(date_str: str) -> Optional[str]:
    if not date_str: return None
    cleaned = re.sub(r'[«»"\'`]', '', date_str).strip()
    if not cleaned: return None
    months = {
        'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
        'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
        'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
    }
    for ru, num in months.items():
        if ru in cleaned.lower():
            parts = cleaned.lower().replace(ru, '').split()
            day = int(parts[0])
            year = int(parts[-1])
            return f"{year}-{num:02d}-{day:02d}"
    return cleaned

# Заглушки для кастомных обработчиков
async def handle_achievement_field(*args): pass
async def handle_opponent_field(*args): pass
# ...

MAPPING: Dict[str, Dict[str, Any]] = {
    # Диссовет
    "DS_number": {"type": "simple", "table": "dissertation_council", "column": "number", "id_column": "id", "id_getter": get_council_id},
    "DS_chairman_degree": {"type": "simple", "table": "person", "column": "degree", "id_column": "id", "id_getter": get_chairman_id},
    "DS_secretary_degree": {"type": "simple", "table": "person", "column": "degree", "id_column": "id", "id_getter": get_secretary_id},

    # Соискатель
    "applicant_email": {"type": "simple", "table": "person", "column": "email", "id_column": "id", "id_getter": get_applicant_id},
    "applicant_phone_number": {"type": "simple", "table": "person", "column": "phone_number", "id_column": "id", "id_getter": get_applicant_id},
    "applicant_full_name_I": {"type": "full_name", "id_getter": get_applicant_id},

    # Диссертация
    "thesis_title": {"type": "simple", "table": "thesis", "column": "title", "id_column": "id", "id_getter": get_thesis_id},
    "degree_R": {"type": "simple", "table": "thesis", "column": "target_degree", "id_column": "id", "id_getter": get_thesis_id},
    "planned_defence_date": {"type": "simple", "table": "thesis", "column": "planned_defence_date", "id_column": "id", "id_getter": get_thesis_id, "transform": parse_russian_date},

    # Руководитель
    "advisor_degree": {"type": "simple", "table": "person", "column": "degree", "id_column": "id", "id_getter": get_supervisor_id},
    "advisor_title": {"type": "simple", "table": "person", "column": "academic_title", "id_column": "id", "id_getter": get_supervisor_id},
    "advisor_name_full": {"type": "full_name", "id_getter": get_supervisor_id},
}