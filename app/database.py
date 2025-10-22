# Verbindung zur Datenbank (PostgreSQL)
# Engine, Session und Base für SQLAlchemy + get_db Dependency.

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session



# Lädt die Variablen aus der .env-Datei (z. B. Datenbank-URL)
load_dotenv()

# Liest die Verbindung (Connection String) aus der Umgebungsvariable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL ist nicht gesetzt. Bitte .env prüfen.")

# 🔹 Engine zuerst erstellen (WICHTIG)
engine = create_engine(DATABASE_URL)

# 🔹 Session-Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔹 Base für Models
Base = declarative_base()

# 🔹 Dependency für DB-Session pro Request
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()