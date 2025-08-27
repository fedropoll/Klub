# Используем Python 3.11 slim
FROM python:3.11-slim

# Создаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости проекта
COPY requirements.txt .

# Устанавливаем pip-зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем папку для медиа
RUN mkdir -p /app/media

# Открываем порт
EXPOSE 8000

# Команда запуска
CMD ["gunicorn", "safe.wsgi:application", "--bind", "0.0.0.0:8000"]
