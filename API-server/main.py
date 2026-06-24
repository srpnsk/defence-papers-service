# main.py
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from database import database
from models import ThesisFormData, ThesisCreate, UserInfo

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
    auth,
)
from form_handler import process_thesis_form
from routers.theses import create_thesis as create_thesis_router
from utils import parse_russian_date
from data_assembler import assemble_full_thesis_json
from routers.auth import get_current_user
from latex_compiler import LatexCompiler

compiler = LatexCompiler(
    temp_base="./temp_latex", 
    project_root=os.path.abspath("./latex_files") 
)

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

# CORS с поддержкой кук
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://185.11.247.199:8080"],   # адрес фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем CRUD-роутеры и аутентификацию
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
# Эндпоинты, доступные только авторизованным пользователям
# ----------------------------------------------------------------------

class TexData(BaseModel):
    # Позволяет принимать динамические ключи вида {"Sources/file.tex": "текст"}
    class Config:
        extra = "allow"

@app.post("/api/compile")
async def compile_latex(data: dict, background_tasks: BackgroundTasks):
    # 1. Запускаем компиляцию
    # Передаем словарь напрямую в ваш метод
    results = compiler.compile_from_files(data)
    
    work_dir = results.get("work_dir")
    pdf_zip_path = results.get("pdf_zip")
    
    # Если в логах есть ошибки или архив не создался
    if not pdf_zip_path or not os.path.exists(pdf_zip_path):
        # Перед паникой логируем ошибки компиляции
        errors = "\n".join(results.get("logs", []))
        # На всякий случай чистим папку, так как эндпоинт прервется
        compiler.cleanup(work_dir)
        raise HTTPException(
            status_code=422, 
            detail=f"Ошибка компиляции документов. Логи:\n{errors}"
        )
    
    # 2. Добавляем фоновую задачу на удаление временной папки ПОСЛЕ того, как файл улетит клиенту
    background_tasks.add_task(compiler.cleanup, work_dir)
    
    # 3. Отправляем ZIP-архив с готовыми PDF обратно фронтенду
    return FileResponse(
        path=pdf_zip_path, 
        filename="compiled_documents.zip", 
        media_type="application/zip"
    )

@app.get("/api/my-theses", tags=["User Theses"])
async def get_my_theses(user: UserInfo = Depends(get_current_user)):
    """
    Возвращает список диссертаций, принадлежащих текущему пользователю.
    """
    # Получаем person_id пользователя
    person_row = await database.fetch_one(
        "SELECT person_id FROM users WHERE id = :user_id", {"user_id": user.user_id}
    )
    if not person_row:
        raise HTTPException(status_code=404, detail="Пользователь не связан с персоной")
    applicant_id = person_row["person_id"]

    query = """
        SELECT id, title, target_degree, planned_defence_date
        FROM thesis
        WHERE applicant_id = :applicant_id
        ORDER BY id DESC
    """
    rows = await database.fetch_all(query, {"applicant_id": applicant_id})
    return [dict(row) for row in rows]


@app.post("/api/thesis/form-data", tags=["Thesis Form"], status_code=201)
async def create_thesis_from_form(
    form_data: ThesisFormData,
    user: UserInfo = Depends(get_current_user)
):
    """
    Создаёт новую диссертацию, автоматически привязывая её к текущему пользователю.
    """
    data_dict = form_data.dict(by_alias=True)

    # Получаем person_id текущего пользователя (он же соискатель)
    person_row = await database.fetch_one(
        "SELECT person_id FROM users WHERE id = :user_id", {"user_id": user.user_id}
    )
    if not person_row:
        raise HTTPException(status_code=400, detail="Пользователь не связан с персоной")
    applicant_id = person_row["person_id"]

    # Специальность диссертации
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

    # Диссовет
    council_number = data_dict.get("DS_number", "")
    council_row = await database.fetch_one(
        "SELECT id FROM dissertation_council WHERE number = :number", {"number": council_number}
    )
    if not council_row:
        raise HTTPException(status_code=400, detail=f"Диссовет с номером '{council_number}' не найден")
    council_id = council_row["id"]

    # Создаём диссертацию
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

    # Полная обработка формы (соискатель, руководитель, оппоненты и т.д.)
    await process_thesis_form(thesis_id, data_dict)

    return {
        "status": "success",
        "message": f"Диссертация создана с ID {thesis_id}",
        "thesis_id": thesis_id
    }


@app.post("/api/thesis/{thesis_id}/form-data", tags=["Thesis Form"])
async def update_thesis_from_form(
    thesis_id: int,
    form_data: ThesisFormData,
    user: UserInfo = Depends(get_current_user)
):
    """
    Обновляет диссертацию, предварительно проверив, что она принадлежит текущему пользователю.
    """
    data_dict = form_data.dict(by_alias=True)

    # Получаем person_id текущего пользователя
    person_row = await database.fetch_one(
        "SELECT person_id FROM users WHERE id = :user_id", {"user_id": user.user_id}
    )
    if not person_row:
        raise HTTPException(status_code=400, detail="Пользователь не связан с персоной")
    applicant_id = person_row["person_id"]

    # Проверяем владельца диссертации
    owner_check = await database.fetch_one(
        "SELECT applicant_id FROM thesis WHERE id = :id", {"id": thesis_id}
    )
    if not owner_check or owner_check["applicant_id"] != applicant_id:
        raise HTTPException(status_code=403, detail="У вас нет прав на эту диссертацию")

    await process_thesis_form(thesis_id, data_dict)
    return {"status": "success", "message": f"Данные диссертации {thesis_id} обновлены"}


@app.get("/api/thesis/{thesis_id}/form-data", tags=["Thesis Form"])
async def get_thesis_form_data(
    thesis_id: int,
    user: UserInfo = Depends(get_current_user)
):
    """
    Возвращает полный JSON диссертации, но только если она принадлежит текущему пользователю.
    """
    person_row = await database.fetch_one(
        "SELECT person_id FROM users WHERE id = :user_id", {"user_id": user.user_id}
    )
    if not person_row:
        raise HTTPException(status_code=400, detail="Пользователь не связан с персоной")
    applicant_id = person_row["person_id"]

    owner_check = await database.fetch_one(
        "SELECT applicant_id FROM thesis WHERE id = :id", {"id": thesis_id}
    )
    if not owner_check or owner_check["applicant_id"] != applicant_id:
        raise HTTPException(status_code=403, detail="Доступ запрещён")

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
