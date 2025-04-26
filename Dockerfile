# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Указываем порт, который будет использовать приложение
EXPOSE 5000

# Команда для запуска приложения
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]