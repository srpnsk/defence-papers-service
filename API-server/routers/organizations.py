from fastapi import APIRouter, HTTPException, Query
from typing import List
from database import database
from models import OrganizationCreate, OrganizationUpdate, OrganizationOut

router = APIRouter(prefix="/organizations", tags=["organizations"])

@router.get("/", response_model=List[OrganizationOut])
async def list_organizations(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    query = "SELECT * FROM organization ORDER BY id LIMIT :limit OFFSET :skip"
    rows = await database.fetch_all(query, {"limit": limit, "skip": skip})
    return [dict(r) for r in rows]

@router.get("/{org_id}", response_model=OrganizationOut)
async def get_organization(org_id: int):
    query = "SELECT * FROM organization WHERE id = :id"
    row = await database.fetch_one(query, {"id": org_id})
    if not row:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return dict(row)

@router.post("/", response_model=OrganizationOut, status_code=201)
async def create_organization(org: OrganizationCreate):
    query = """
        INSERT INTO organization (full_name, short_name, address)
        VALUES (:full_name, :short_name, :address)
        RETURNING id
    """
    new_id = await database.execute(query, org.dict())
    return await get_organization(new_id)

@router.put("/{org_id}", response_model=OrganizationOut)
async def update_organization(org_id: int, org: OrganizationUpdate):
    await get_organization(org_id)
    updates = {k: v for k, v in org.dict(exclude_unset=True).items() if v is not None}
    if not updates:
        return await get_organization(org_id)
    set_clause = ", ".join(f"{k} = :{k}" for k in updates)
    query = f"UPDATE organization SET {set_clause} WHERE id = :id"
    values = {**updates, "id": org_id}
    await database.execute(query, values)
    return await get_organization(org_id)

@router.delete("/{org_id}", status_code=204)
async def delete_organization(org_id: int):
    await get_organization(org_id)
    query = "DELETE FROM organization WHERE id = :id"
    await database.execute(query, {"id": org_id})
    return