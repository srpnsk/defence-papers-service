from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.core.config import settings
from app.schemas.documents import DocumentFormat
from app.services.document_conversion import (
    DocumentConversionService,
)
from app.storage.filesystem import FileStorage

router = APIRouter()


def get_storage() -> FileStorage:
    return FileStorage(settings.documents_path)


def get_conversion_service() -> DocumentConversionService:
    return DocumentConversionService()


@router.post("/documents/compile")
def compile_document(
        filename: str,
        output_format: DocumentFormat = Query(...),
        storage: FileStorage = Depends(get_storage),
        conversion_service: DocumentConversionService = Depends(
            get_conversion_service
        ),
):
    try:
        file_path = storage.get(filename)

        document = conversion_service.convert(
            file_path=file_path,
            output_format=output_format,
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return StreamingResponse(
        document,
        media_type=_get_media_type(output_format),
        headers={
            "Content-Disposition": (
                f'attachment; filename="{_output_filename(filename, output_format)}"'
            )
        },
    )


def _get_media_type(
        output_format: DocumentFormat,
) -> str:
    return {
        DocumentFormat.PDF: "application/pdf",
        DocumentFormat.DOCX: (
            "application/"
            "vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),
    }[output_format]


def _output_filename(
        filename: str,
        output_format: DocumentFormat,
) -> str:
    return (
        f"{filename.rsplit('.', 1)[0]}"
        f".{output_format.value}"
    )
