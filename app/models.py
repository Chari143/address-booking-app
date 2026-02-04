
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from .database import Base


class Address(Base):
    """
    Stores standard address fields, geographic coordinates
    for location-based queries.
    """
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Address(id={self.id}, street='{self.street}', city='{self.city}')>"

