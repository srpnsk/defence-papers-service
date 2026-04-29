# main.py
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from typing import Dict, Any

from database import database
from models import ThesisFormData
from field_mapping import MAPPING
from data_assembler import assemble_thesis_json

# Импорт роутеров для всех сущностей
from routers import (
    persons,
    organizations,
    specialties,
    councils,
    theses,
    achievements,
    employments,
    educations,
    applicant_details,
)

# =============================================================================
# Настройка lifespan для подключения/отключения БД
# =============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(
    title="Dissertation Council API",
    description="API для управления диссертационным советом",
    version="1.0.0",
    lifespan=lifespan,
)

# =============================================================================
# Подключение роутеров
# =============================================================================
app.include_router(persons.router)
app.include_router(organizations.router)
app.include_router(specialties.router)
app.include_router(councils.router)
app.include_router(theses.router)
app.include_router(achievements.router)
app.include_router(employments.router)
app.include_router(educations.router)
app.include_router(applicant_details.router)

# =============================================================================
# Вспомогательная функция для получения контекста диссертации
# =============================================================================
async def get_thesis_context(thesis_id: int) -> dict:
    query = """
        SELECT 
            t.id AS thesis_id,
            t.applicant_id,
            t.council_id,
            t.specialty_id,
            dc.chairman_id,
            dc.secretary_id,
            (SELECT tp.person_id FROM thesis_participation tp 
             WHERE tp.thesis_id = t.id AND tp.role = 'supervisor' LIMIT 1) AS supervisor_id,
            (SELECT jsonb_object_agg(too.order_index::text, too.person_id) 
             FROM thesis_official_opponent too WHERE too.thesis_id = t.id) AS opponents
        FROM thesis t
        JOIN dissertation_council dc ON t.council_id = dc.id
        WHERE t.id = :id
    """
    row = await database.fetch_one(query, {"id": thesis_id})
    if not row:
        raise HTTPException(status_code=404, detail="Диссертация не найдена")

    ctx = {
        "thesis_id": row["thesis_id"],
        "applicant_id": row["applicant_id"],
        "council_id": row["council_id"],
        "specialty_id": row["specialty_id"],
        "chairman_id": row["chairman_id"],
        "secretary_id": row["secretary_id"],
        "supervisor_id": row["supervisor_id"],
    }
    opponents = row["opponents"] or {}
    for i in range(1, 4):
        ctx[f"opponent_{i}_id"] = opponents.get(str(i))
    return ctx

# =============================================================================
# Применение обновлений по маппингу полей формы
# =============================================================================
async def apply_form_updates(thesis_id: int, form_data: dict):
    ctx = await get_thesis_context(thesis_id)
    async with database.transaction():
        for field_id, value in form_data.items():
            if field_id not in MAPPING:
                continue
            rule = MAPPING[field_id]
            if rule["type"] == "simple":
                record_id = rule["id_getter"](ctx)
                if record_id is None:
                    continue
                if "transform" in rule:
                    value = rule["transform"](value)
                query = f"UPDATE {rule['table']} SET {rule['column']} = :val WHERE {rule['id_column']} = :id"
                await database.execute(query, {"val": value, "id": record_id})
            elif rule["type"] == "full_name":
                record_id = rule["id_getter"](ctx)
                if record_id is None:
                    continue
                parts = value.strip().split()
                if len(parts) >= 2:
                    await database.execute(
                        "UPDATE person SET last_name=:l, first_name=:f, second_name=:s WHERE id=:id",
                        {
                            "l": parts[0],
                            "f": parts[1],
                            "s": parts[2] if len(parts) > 2 else None,
                            "id": record_id,
                        },
                    )
            elif rule["type"] == "custom":
                # Кастомные обработчики реализуются в field_mapping
                if "handler" in rule:
                    await rule["handler"](thesis_id, field_id, value, ctx, database)

# =============================================================================
# Эндпоинты для работы с формой диссертации (большой JSON)
# =============================================================================
@app.post("/api/thesis/{thesis_id}/form-data", tags=["Thesis Form"])
async def save_thesis_form_data(thesis_id: int, form_data: ThesisFormData):
    """
    Принимает полный JSON формы (400+ полей) и обновляет все связанные таблицы БД.
    """
    data_dict = form_data.dict(by_alias=True)
    await apply_form_updates(thesis_id, data_dict)
    return {"status": "success", "message": f"Данные диссертации {thesis_id} обновлены"}

@app.get("/api/thesis/{thesis_id}/form-data", tags=["Thesis Form"])
async def get_thesis_form_data(thesis_id: int):
    """
    Возвращает полный JSON формы, собранный из нормализованных таблиц БД.
    """
    data = await assemble_thesis_json(thesis_id)
    if not data:
        raise HTTPException(status_code=404, detail="Данные формы не найдены")
    return data

# =============================================================================
# Корневой эндпоинт
# =============================================================================
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "API диссертационного совета работает (надеюсь) ",
        "docs": "/docs"
    }