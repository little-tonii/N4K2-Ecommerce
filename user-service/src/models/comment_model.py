from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.sql import func
from ..configs.database import Base

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
