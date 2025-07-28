from app.db.session import engine
from app.db.session import Base
from app.models.request_log import RequestLog
from app.models.user import User


print("Model importat:", RequestLog.__tablename__)


def init_db():
    # Creează toate tabelele definite cu Base
    Base.metadata.create_all(bind=engine, checkfirst=False)  # forțăm crearea


init_db()
