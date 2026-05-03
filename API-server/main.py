# main.py
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from database import database
from models import ThesisFormData, ThesisCreate, PersonCreate

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
    auth
)
from form_handler import process_thesis_form
from routers.persons import create_person
from routers.theses import create_thesis as create_thesis_router
from utils import parse_full_name, parse_russian_date
from data_assembler import assemble_full_thesis_json


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

# CORS – разрешает запросы с любого источника (при необходимости сузьте)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Стандартные CRUD-роутеры
app.include_router(persons.router)
app.include_router(organizations.router)
app.include_router(specialties.router)
app.include_router(councils.router)
app.include_router(theses.router)
app.include_router(achievements.router)
app.include_router(employments.router)
app.include_router(educations.router)
app.include_router(applicant_details.router)
app.include_router(auth.router)


# ----------------------------------------------------------------------
# Эндпоинты для работы с полной формой
# ----------------------------------------------------------------------
@app.post("/api/thesis/form-data", tags=["Thesis Form"], status_code=201)
async def create_thesis_from_form(form_data: ThesisFormData):
    """
    Создаёт новую диссертацию и все связанные записи из полной формы.
    Возвращает ID созданной диссертации.
    """
    data_dict = form_data.dict(by_alias=True)

    # 1. Соискатель
    applicant_name = parse_full_name(data_dict.get("applicant_full_name_I", ""))
    if not applicant_name:
        raise HTTPException(status_code=400, detail="Не заполнено ФИО соискателя")

    # Ищем существующего соискателя по фамилии и имени
    existing_applicant = await database.fetch_one(
        "SELECT id FROM person WHERE last_name = :last_name AND first_name = :first_name",
        {"last_name": applicant_name["last_name"], "first_name": applicant_name["first_name"]}
    )
    if existing_applicant:
        applicant_id = existing_applicant["id"]
    else:
        new_applicant = await create_person(PersonCreate(
            last_name=applicant_name["last_name"],
            first_name=applicant_name["first_name"],
            second_name=applicant_name.get("second_name"),
            email=data_dict.get("applicant_email"),
            phone_number=data_dict.get("applicant_phone_number"),
            specialty_id=None
        ))
        applicant_id = new_applicant["id"]

    # 2. Специальность диссертации
    spec_code = data_dict.get("applicant_specialty_number", "")
    spec_row = await database.fetch_one(
        "SELECT id FROM specialty WHERE code = :code", {"code": spec_code}
    )
    if not spec_row:
        new_spec = await database.execute(
            "INSERT INTO specialty (code, name) VALUES (:code, :name) RETURNING id",
            {"code": spec_code, "name": data_dict.get("applicant_specialty_title", spec_code)}
        )
        specialty_id = new_spec
    else:
        specialty_id = spec_row["id"]

    # 3. Диссертационный совет
    council_number = data_dict.get("DS_number", "")
    council_row = await database.fetch_one(
        "SELECT id FROM dissertation_council WHERE number = :number", {"number": council_number}
    )
    if not council_row:
        raise HTTPException(status_code=400, detail=f"Диссовет с номером '{council_number}' не найден")
    council_id = council_row["id"]

    # 4. Создаём диссертацию
    thesis_create = ThesisCreate(
        applicant_id=applicant_id,
        council_id=council_id,
        title=data_dict.get("thesis_title", "Без названия"),
        science_branch=data_dict.get("applicant_speciality_type", "физико-математические"),
        target_degree=data_dict.get("degree_R", "кандидата наук"),
        planned_defence_date=parse_russian_date(data_dict.get("planned_defence_date")),
        defence_date_time=None,
        specialty_id=specialty_id,
    )
    new_thesis = await create_thesis_router(thesis_create)
    thesis_id = new_thesis["id"]

    # 5. Применить полную обработку формы
    await process_thesis_form(thesis_id, data_dict)

    return {
        "status": "success",
        "message": f"Диссертация создана с ID {thesis_id}",
        "thesis_id": thesis_id
    }


@app.post("/api/thesis/{thesis_id}/form-data", tags=["Thesis Form"])
async def update_thesis_from_form(thesis_id: int, form_data: ThesisFormData):
    """
    Обновляет существующую диссертацию и все связанные записи из полной формы.
    """
    data_dict = form_data.dict(by_alias=True)
    await process_thesis_form(thesis_id, data_dict)
    return {"status": "success", "message": f"Данные диссертации {thesis_id} обновлены"}


@app.get("/api/thesis/{thesis_id}/form-data", tags=["Thesis Form"])
async def get_thesis_form_data(thesis_id: int):
    """
    Возвращает полный JSON формы, собранный из всех таблиц БД.
    """
    data = await assemble_full_thesis_json(thesis_id)
    if not data:
        raise HTTPException(status_code=404, detail="Данные формы не найдены")
    return data


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "API диссертационного совета работает (надеюсь) ",
        "docs": "/docs"
    }
