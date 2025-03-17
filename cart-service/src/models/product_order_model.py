from sqlalchemy import Column, ForeignKey, Integer, String
from ..configs.database import Base

class ProductOrderModel(Base):
    __tablename__ = "product_order"
    
    id: int = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    product_id: str = Column(String, nullable=False, index=True)
    order_id: int = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    quantity: int = Column(Integer, default=1, nullable=False)
    price: int = Column(Integer, nullable=False)