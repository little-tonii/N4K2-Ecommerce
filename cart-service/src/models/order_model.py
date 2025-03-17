from sqlalchemy import Column, Enum, Integer, String
from ..configs.database import Base
import enum

class OrderStatus(enum.Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELED = "canceled"

class OrderModel(Base):
    __tablename__ = "orders"
    
    id: int = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    user_id: int = Column(Integer, nullable=False)
    total_price: int = Column(Integer, nullable=False)
    phone_number: str = Column(String, nullable=False)
    address: str = Column(String, nullable=False)
    full_name: str = Column(String, nullable=False)
    status: str = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)