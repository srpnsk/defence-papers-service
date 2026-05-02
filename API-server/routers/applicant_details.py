from fastapi import APIRouter, HTTPException, Query
from typing import List
from database import database
from models import ApplicantDetailsCreate, ApplicantDetailsUpdate, ApplicantDetailsOut

router = APIRouter(prefix="/applicant-details", tags=["applicant_details"])

@router.get("/", response_model=List[ApplicantDetailsOut])
async def list_details(skip: int = 0, limit: int = 100):
    query = "SELECT * FROM applicant_details ORDER BY person_id LIMIT :limit OFFSET :skip"
    rows = await database.fetch_all(query, {"limit": limit, "skip": skip})
    return [dict(r) for r in rows]

@router.get("/{person_id}", response_model=ApplicantDetailsOut)
async def get_details(person_id: int):
    query = "SELECT * FROM applicant_details WHERE person_id = :pid"
    row = await database.fetch_one(query, {"pid": person_id})
    if not row:
        raise HTTPException(status_code=404, detail="Детали соискателя не найдены")
    return dict(row)

@router.post("/", response_model=ApplicantDetailsOut, status_code=201)
async def create_details(details: ApplicantDetailsCreate):
    # Проверка, что такой person_id существует
    person_check = await database.fetch_one("SELECT id FROM person WHERE id = :id", {"id": details.person_id})
    if not person_check:
        raise HTTPException(status_code=400, detail="Персона с указанным ID не существует")
    query = """
        INSERT INTO applicant_details (person_id, snils, passport_type, passport_series, passport_number, home_address, sex, birth_date, is_postgrad_completed, postgrad_end_date)
        VALUES (:person_id, :snils, :passport_type, :passport_series, :passport_number, :home_address, :sex, :birth_date, :is_postgrad_completed, :postgrad_end_date)
        RETURNING person_id
    """
    values = details.dict()
    await database.execute(query, values)
    return await get_details(details.person_id)

@router.put("/{person_id}", response_model=ApplicantDetailsOut)
async def update_details(person_id: int, details: ApplicantDetailsUpdate):
    await get_details(person_id)
    updates = {k: v for k, v in details.dict(exclude_unset=True).items() if v is not None}
    if not updates:
        return await get_details(person_id)
    set_clause = ", ".join(f"{k} = :{k}" for k in updates)
    query = f"UPDATE applicant_details SET {set_clause} WHERE person_id = :person_id"
    values = {**updates, "person_id": person_id}
    await database.execute(query, values)
    return await get_details(person_id)

@router.delete("/{person_id}", status_code=204)
async def delete_details(person_id: int):
    await get_details(person_id)
    query = "DELETE FROM applicant_details WHERE person_id = :person_id"
    await database.execute(query, {"person_id": person_id})
    return