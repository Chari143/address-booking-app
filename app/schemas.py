
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class AddressBase(BaseModel):
    street: str = Field(..., min_length=1, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180, description="Longitude (-180 to 180)")


class AddressCreate(AddressBase):
    pass



class AddressUpdate(BaseModel):
    street: Optional[str] = Field(None, min_length=1, max_length=255)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, min_length=1, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

    @field_validator('latitude', 'longitude', mode='before')
    @classmethod
    def check_coordinates(cls, v):
        if v is not None and not isinstance(v, (int, float)):
            raise ValueError('Coordinates must be numbers')
        return v


class AddressResponse(AddressBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NearbySearchParams(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    distance_km: float = Field(..., gt=0, le=20000)
