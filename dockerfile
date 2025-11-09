FROM python:3.11-slim

# Устанавливаем системные зависимости для vosk (если нужно)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    portaudio19-dev \
    python3-pyaudio \
    ffmpeg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем ВСЮ папку app в контейнер
COPY ./app/ .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Запускаем генерацию конфига и приложение
CMD ["uvicorn", "main:fastapi_app", "--host", "0.0.0.0", "--port", "8000"]