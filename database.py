import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

from models import User, Product

# 1. Cargamos las variables secretas desde el archivo .env
load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# 2. Construimos la URL usando las variables secretas sin exponer la contraseña
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# 3. Creamos el motor de SQLModel / SQLAlchemy
engine = create_engine(DATABASE_URL)

def init_db():
    """Crea las tablas en Supabase."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Inyección de dependencia para obtener la sesión en FastAPI."""
    with Session(engine) as session:
        yield session

# Bloque para probar la conexión de manera segura
if __name__ == "__main__":
    print("Creando tablas en Supabase...")
    init_db()
    print("¡Tablas creadas con éxito!")