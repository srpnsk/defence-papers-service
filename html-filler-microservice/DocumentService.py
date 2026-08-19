from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined


class TemplateStorage:
    def __init__(self, templates_dir: str = "templates", output_dir: str = "output") -> None:
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_template(self, template_name: str) -> str:
        file_path = self.templates_dir / f"{template_name}.txt"
        if not file_path.exists():
            raise FileNotFoundError(f"Шаблон '{file_path}' не найден.")
        return file_path.read_text(encoding="utf-8")

    def save_result(self, filename: str, content: str) -> Path:
        output_path = self.output_dir / filename
        output_path.write_text(content, encoding="utf-8")
        return output_path.resolve()


class TemplateRenderer:
    def __init__(self, templates_dir: str) -> None:
        self.environment = Environment(
            loader=FileSystemLoader(templates_dir),
            undefined=StrictUndefined,
            autoescape=False,
        )

    def render(self, template_name: str, values: dict) -> str:
        template = self.environment.get_template(
            f"{template_name}.html"
        )

        return template.render(**values)


class DocumentService:
    def __init__(self, st0rage: TemplateStorage, renderer: type[TemplateRenderer] = TemplateRenderer) -> None:
        self.storage = st0rage
        self.renderer = renderer

    def process_document(self, template_id: str, values: dict, output_filename: str) -> Path:
        rendered_content = self.renderer.render(template_id, values)

        return self.storage.save_result(output_filename, rendered_content)


storage = TemplateStorage(templates_dir="./templates", output_dir="./tmp/compiled_html")
doc_service = DocumentService(st0rage=storage)


# Обработка запроса
def handle_generate_html_request(payload: dict):
    # payload: {"template_id": "invoice_12", "data": {"user_name": "Ivan"}, "output_name": "doc_123.html"}

    saved_path = doc_service.process_document(
        template_id=payload["template_id"],
        values=payload["data"],
        output_filename=payload["output_name"])

    # saved_path -> PosixPath('/app/tmp/compiled_html/doc_123.html')
    # Далее отдаем этот путь компилятору PDF/DOCX
    return str(saved_path)
