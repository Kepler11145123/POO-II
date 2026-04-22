from database.base import Base
from database.connection import engine
from database import models

Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas exitosamente")