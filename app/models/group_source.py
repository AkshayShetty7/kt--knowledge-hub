from sqlalchemy import Column, ForeignKey, String

from app.core.database import Base


class GroupSource(Base):
    __tablename__ = "group_sources"

    group_id = Column(
        String,
        ForeignKey("groups.id", ondelete="CASCADE"),
        primary_key=True,
    )

    source_id = Column(
        String,
        ForeignKey("sources.id", ondelete="CASCADE"),
        primary_key=True,
    )