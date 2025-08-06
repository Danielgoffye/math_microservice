# Imagine de bază oficială cu Python 3.10 (compatibil cu FastAPI 0.95.2 și Pydantic 1.x)
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
