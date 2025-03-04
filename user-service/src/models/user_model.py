from ..configs.database import Base
from sqlalchemy import Column, DateTime, Enum, Integer, String, func
from enum import Enum as PyEnum

class AccountType(PyEnum):
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email: str = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(255), nullable=False)
    refresh_token: str = Column(String(255), nullable=True)
    phone_number: str = Column(String(20), nullable=True)
    address: str = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    account_type: str = Column(Enum(AccountType), nullable=False, default=AccountType.CUSTOMER)