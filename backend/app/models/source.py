from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from app.core.database import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_path = Column(Text, nullable=False)

    status = Column(String, nullable=False, default="processing")

    pages = Column(Integer, default=0)
    chunks = Column(Integer, default=0)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )