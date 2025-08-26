# Используем официальный образ Python
FROM python:3.10-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Открываем порт для Django
EXPOSE 8000

# Команда запуска Django через Gunicorn
CMD ["gunicorn", "safe.wsgi:application", "--bind", "0.0.0.0:8000"]
