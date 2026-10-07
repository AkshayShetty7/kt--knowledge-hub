from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text

from app.core.database import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )