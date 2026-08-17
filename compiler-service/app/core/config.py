from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    documents_path: Path = Path("/documents")

    model_config = {
        "env_prefix": "DOCUMENT_",
    }


settings = Settings()
