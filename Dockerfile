# Используем официальный Python
FROM python:3.10-slim

# Рабочая директория
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Выполняем миграции и сборку статики
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Открываем порт
EXPOSE 8080

# Команда запуска
CMD ["gunicorn", "safe.wsgi:application", "--bind", "0.0.0.0:8080"]
