from fastapi import APIRouter, HTTPException
from typing import List
from database import database
from models import PersonCreate, PersonUpdate, PersonOut

router = APIRouter(prefix="/persons", tags=["persons"])

@router.get("/", response_model=List[PersonOut])
async def list_persons():
    query = "SELECT * FROM person ORDER BY id"
    rows = await database.fetch_all(query)
    return [dict(r) for r in rows]

@router.get("/{person_id}", response_model=PersonOut)
async def get_person(person_id: int):
    query = "SELECT * FROM person WHERE id = :id"
    row = await database.fetch_one(query, {"id": person_id})
    if not row:
        raise HTTPException(status_code=404, detail="Персона не найдена")
    return dict(row)

@router.post("/", response_model=PersonOut, status_code=201)
async def create_person(person: PersonCreate):
    query = """
        INSERT INTO person (last_name, first_name, second_name, degree, academic_title, email, phone_number, specialty_id)
        VALUES (:last_name, :first_name, :second_name, :degree, :academic_title, :email, :phone_number, :specialty_id)
        RETURNING id
    """
    values = person.dict()
    new_id = await database.execute(query, values)
    # Получаем созданную запись
    return await get_person(new_id)

@router.put("/{person_id}", response_model=PersonOut)
async def update_person(person_id: int, person: PersonUpdate):
    # Проверим существование
    await get_person(person_id)  # выбросит 404 если нет
    # Строим динамический UPDATE
    updates = {k: v for k, v in person.dict().items() if v is not None}
    if not updates:
        return await get_person(person_id)
    set_clause = ", ".join(f"{k} = :{k}" for k in updates)
    query = f"UPDATE person SET {set_clause} WHERE id = :id"
    values = {**updates, "id": person_id}
    await database.execute(query, values)
    return await get_person(person_id)

@router.delete("/{person_id}", status_code=204)
async def delete_person(person_id: int):
    await get_person(person_id)  # проверка
    query = "DELETE FROM person WHERE id = :id"
    await database.execute(query, {"id": person_id})
    return