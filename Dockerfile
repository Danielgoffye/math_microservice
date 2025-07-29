# Imagine de bază oficială cu Python 3.10 (compatibil cu FastAPI 0.95.2 și Pydantic 1.x)
FROM python:3.10-slim

# Setăm directorul de lucru din interiorul containerului
WORKDIR /app

# Copiem tot codul tău în container
COPY . .

# Instalăm toate librăriile
RUN pip install --no-cache-dir -r requirements.txt

# Expunem portul aplicației
EXPOSE 8000

# Comanda care pornește serverul FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
