from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URL = (
    f"sqlite:///{os.path.join(BASE_DIR, '../../requests.db')}"
)


# 2. Creăm engine-ul (motorul DB)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Instanțiem "sessionmaker" — creează sesiuni de lucru cu DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. "Base" e clasa de bază pentru toate modelele ORM
Base = declarative_base()
