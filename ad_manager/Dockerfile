FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends postgresql-client \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
  
EXPOSE 2025

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "2025", "core.asgi:application", "--ws", "auto"]