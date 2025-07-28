from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.session import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class RequestLog(Base):
    __tablename__ = "request_logs"  # numele tabelei din DB

    id = Column(
        Integer,  # cheie primară auto-incrementală
        primary_key=True,
        index=True
    )
    operation = Column(
        String,  # 'pow', 'factorial', 'fibonacci'
        nullable=False
    )
    parameters = Column(
        String,  # păstrăm inputul sub formă de text (ex: JSON)
        nullable=False
    )
    result = Column(
        String,  # rezultatul operației
        nullable=False
    )
    timestamp = Column(
        DateTime(timezone=True),  # ora când s-a făcut cererea
        server_default=func.now()
    )
    is_cached = Column(
        Integer,
        default=0
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )
    user = relationship(
        "User",
        backref="logs"
    )
