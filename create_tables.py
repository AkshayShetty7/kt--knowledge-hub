from backend.app.core.database import Base, engine
from backend.app.models import Source, Group, GroupSource

Base.metadata.create_all(bind=engine)

print("Database tables created.")