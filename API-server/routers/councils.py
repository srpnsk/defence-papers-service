from fastapi import APIRouter, HTTPException, Query
from typing import List
from database import database
from models import CouncilCreate, CouncilUpdate, CouncilOut

router = APIRouter(prefix="/councils", tags=["councils"])

@router.get("/", response_model=List[CouncilOut])
async def list_councils(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    query = "SELECT * FROM dissertation_council ORDER BY id LIMIT :limit OFFSET :skip"
    rows = await database.fetch_all(query, {"limit": limit, "skip": skip})
    return [dict(r) for r in rows]

@router.get("/{council_id}", response_model=CouncilOut)
async def get_council(council_id: int):
    query = "SELECT * FROM dissertation_council WHERE id = :id"
    row = await database.fetch_one(query, {"id": council_id})
    if not row:
        raise HTTPException(status_code=404, detail="Диссертационный совет не найден")
    return dict(row)

@router.post("/", response_model=CouncilOut, status_code=201)
async def create_council(council: CouncilCreate):
    query = """
        INSERT INTO dissertation_council (number, organization_id, chairman_id, secretary_id, members_count_total)
        VALUES (:number, :organization_id, :chairman_id, :secretary_id, :members_count_total)
        RETURNING id
    """
    new_id = await database.execute(query, council.dict())
    return await get_council(new_id)

@router.put("/{council_id}", response_model=CouncilOut)
async def update_council(council_id: int, council: CouncilUpdate):
    await get_council(council_id)
    updates = {k: v for k, v in council.dict(exclude_unset=True).items() if v is not None}
    if not updates:
        return await get_council(council_id)
    set_clause = ", ".join(f"{k} = :{k}" for k in updates)
    query = f"UPDATE dissertation_council SET {set_clause} WHERE id = :id"
    values = {**updates, "id": council_id}
    await database.execute(query, values)
    return await get_council(council_id)

@router.delete("/{council_id}", status_code=204)
async def delete_council(council_id: int):
    await get_council(council_id)
    query = "DELETE FROM dissertation_council WHERE id = :id"
    await database.execute(query, {"id": council_id})
    return