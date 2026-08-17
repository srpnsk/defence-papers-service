import io
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Type

from docx import Document
from htmldocx import HtmlToDocx
from weasyprint import HTML
import magic

from app.schemas.documents import DocumentFormat


class DocumentReader:
    @staticmethod
    def read_html(path: Path) -> str:
        if not path.exists():
            raise FileNotFoundError(
                f"HTML файл не найден: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Путь не является файлом: {path}"
            )

        mime_type = magic.from_file(path, mime=True)

        if mime_type != "text/html":
            raise ValueError(
                f"Файл не является HTML документом: {path}"
            )

        return path.read_text(encoding="utf-8")


class BaseConverter(ABC):
    @abstractmethod
    def convert(self, file_path: Path) -> io.BytesIO:
        pass


class PdfConverter(BaseConverter):
    def convert(self, file_path: Path) -> io.BytesIO:
        stream = io.BytesIO()

        HTML(
            filename=str(file_path)
        ).write_pdf(target=stream)

        stream.seek(0)

        return stream


class DocxConverter(BaseConverter):
    def __init__(
            self,
            reader: DocumentReader | None = None,
    ):
        self._reader = reader or DocumentReader()

    def convert(self, file_path: Path) -> io.BytesIO:
        html_content = self._reader.read_html(file_path)

        document = Document()

        parser = HtmlToDocx()
        parser.add_html_to_document(
            html_content,
            document,
        )

        stream = io.BytesIO()
        document.save(stream)

        stream.seek(0)

        return stream


class DocumentConversionService:
    def __init__(self):
        self._converters: dict[
            DocumentFormat,
            Type[BaseConverter],
        ] = {
            DocumentFormat.PDF: PdfConverter,
            DocumentFormat.DOCX: DocxConverter,
        }

    def convert(
            self,
            file_path: Path,
            output_format: DocumentFormat,
    ) -> io.BytesIO:
        converter_cls = self._converters.get(output_format)

        if converter_cls is None:
            raise ValueError(
                f"Unsupported format: {output_format}"
            )

        converter = converter_cls()

        return converter.convert(file_path)
