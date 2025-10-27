# Diese Klasse gehört zu SQLAlchemy (ORM).
# Sie stellt eine Tabelle in der Datenbank.
# Die Spalten werden mit Column(...) definiert.
# Über diese Klasse führt man CRUD-Operationen aus (Create, Read, Update, Delete).


from sqlalchemy import (
    Column, Integer, String, Date, DateTime, func,
    CheckConstraint, UniqueConstraint, Index
)
from .database import Base

#Tabelle "employees" wird hier definiert
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False, index=True)  
    last_name = Column(String(100), nullable=False, index=True)   
    age = Column(Integer, nullable=True)
    gender = Column(String(20), nullable=True)
    email = Column(String(150), nullable=False, unique=True)
    birth_date = Column(Date, nullable=True)
    phone_number = Column(String(20), unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("age IS NULL OR (age >= 16 AND age <= 120)", name="ck_emp_age"),
        CheckConstraint("phone_number IS NULL OR phone_number ~ '^[+0-9]{6,20}$'", name="ck_emp_phone"),
        CheckConstraint("first_name ~ '^[A-Za-zÄÖÜäöüß\\- ]{1,100}$'", name="ck_emp_first_name"),
        CheckConstraint("last_name  ~ '^[A-Za-zÄÖÜäöüß\\- ]{1,100}$'", name="ck_emp_last_name"),

        
        Index(
            "uq_emp_fullname_ci",
            func.lower(first_name),
            func.lower(last_name),
            unique=True
        ),

        Index("ix_emp_last_name_only", "last_name"),
    )
