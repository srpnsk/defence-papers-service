FROM python:3.10-slim

# Установка системных зависимостей для LaTeX (если нужно)
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-fonts-recommended \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY API-server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь исходный код сервера
COPY API-server/ .

# Команда запуска из твоих инструкций
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8087"]
