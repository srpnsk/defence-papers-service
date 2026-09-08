'''
В этой директории пишем классы пустышки, как бы контракты
пример:

from pydantic import BaseModel, Field
from typing import Dict, Any

class DocumentGenerateRequest(BaseModel):
    template_id: str = Field(..., example="invoice_v1")
    data: Dict[str, Any] = Field(..., example={"client_name": "Иван", "amount": 1000})

class DocumentGenerateResponse(BaseModel):
    file_path: str
    status: str = "success"
'''
