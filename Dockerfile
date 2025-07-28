# Imagine de bază oficială cu Python 3.12
FROM python:3.12-slim

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
