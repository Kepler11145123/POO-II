from database.connection import engine

try:
    with engine.connect() as conn:
        print("✅ Conexión exitosa a PostgreSQL")
except Exception as e:
    print(f"❌ Error: {e}")