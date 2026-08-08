'''
Здесь пишем пути к папкам, порты, URL интеграций и прочие настройки
важно: В микросервисах все параметры должны читаться из переменных окружения (.env).
вот пример:

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Document Generator Service"
    TEMPLATES_DIR: str = "./templates"
    OUTPUT_DIR: str = "./tmp/output"
    DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
'''

''' ну так должны читаться с env, а в твоём примере они прописаны в коде ;)'''
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent.parent # директория с .env

class Settings(BaseSettings):

    PROJECT_NAME: str = "Document Generator Service"
    TEMPLATES_DIR: str = "./templates"
    OUTPUT_DIR: str = "./tmp/output"
    DEBUG: bool = False
    ALLOW_METHODS: List[str] = ["*"]
    ALLOW_HEADERS: List[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True

    # Сюда автоматически загрузится список из .env
    BACKEND_CORS_ORIGINS: List[str] = []

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"), 
        env_file_encoding='utf-8'
    )


# Создаем объект настроек, который будем импортировать в другие файлы
settings = Settings()
print(settings.TEMPLATES_DIR) # для теста