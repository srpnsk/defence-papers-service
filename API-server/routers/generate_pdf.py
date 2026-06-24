
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

router = APIRouter()

@router.post("/api/thesis/generate-pdf")
async def generate_thesis_pdf(data: dict):
    try:
        # Твой LatexCompiler должен уметь принимать словарь данных
        # и возвращать путь к готовому файлу или байты
        compiler = LatexCompiler(template_data=data)
        pdf_path = compiler.compile() 
        
        with open(pdf_path, "rb") as f:
            pdf_content = f.read()
            
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=thesis.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
