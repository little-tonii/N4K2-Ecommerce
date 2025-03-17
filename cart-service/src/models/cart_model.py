from sqlalchemy import Column, Integer
from ..configs.database import Base

class CartModel(Base):
    __tablename__ = "carts"
    
    id: int = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    user_id: int = Column(Integer, nullable=False, index=True)
    