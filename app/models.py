# Diese Klasse gehört zu SQLAlchemy (ORM).
# Sie stellt eine Tabelle in der Datenbank.
# Die Spalten werden mit Column(...) definiert.
# Über diese Klasse führt man CRUD-Operationen aus (Create, Read, Update, Delete).


from sqlalchemy import Column, Integer, String, Date, DateTime, func
from .database import Base

#Tabelle "employees" wird hier definiert
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False, index=True)
    last_name  = Column(String(100), nullable=False, index=True)
    age        = Column(Integer, nullable=True)
    gender     = Column(String(20), nullable=True)
    email      = Column(String(150), unique=True)
    birth_date = Column(Date, nullable=True)   
    phone_number = Column(String(20), unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
