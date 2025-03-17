from sqlalchemy import Column, ForeignKey, Integer, String
from ..configs.database import Base

class ProductCartModel(Base):
    __tablename__ = "product_cart"
    
    id: int = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    product_id: str = Column(String, nullable=False, index=True)
    cart_id: int = Column(Integer, ForeignKey("carts.id"), nullable=False, index=True)
    quantity: int = Column(Integer, default=1, nullable=False)
    price: int = Column(Integer, nullable=False)