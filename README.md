# Math Microservice

Un microserviciu REST complet pentru efectuarea de operații matematice de bază (putere, factorial, fibonacci), cu interfață web, autentificare JWT, Redis caching, istoric, metrici și containerizare Docker.

---

## Funcționalități principale

-  Operații: `pow(base, exp)`, `factorial(n)`, `fibonacci(n)`
-  Autentificare cu JWT (login / register)
-  Caching persistent cu Redis
-  Istoric calcule per utilizator
-  Statistici cu cache hit rate + distribuție operații
-  UI HTML complet (login, register, home, history, metrics)
-  Docker + docker-compose ready
-  Export istoric în JSON

---

##  Structură proiect

    math_microservice/
    ├── app/
    │ ├── main.py
    │ ├── api/ # Endpoints (auth, UI, logică)
    │ ├── services/ # Calcul logic & Redis
    │ ├── templates/ # HTML-uri
    │ ├── models/ # ORM: User, Logs
    │ └── ... # config, db, auth
    ├── Dockerfile
    ├── docker-compose.yml
    ├── requirements.txt
    └── README.md


---

##  Cum rulezi local (fără Docker)

```bash

python -m venv venv

venv\Scripts\activate   # Windows

pip install -r requirements.txt

uvicorn app.main:app --reload

Aplicația va fi accesibilă la: http://localhost:8000


## Cum rulezi cu Docker

```bash

docker-compose build

docker-compose up

Aplicația va fi accesibilă la: http://localhost:8000
