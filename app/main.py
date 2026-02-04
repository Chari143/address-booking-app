
import logging
from typing import List

from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from .database import get_db, init_db
from .models import Address
from .schemas import AddressCreate, AddressUpdate, AddressResponse
from .utils import haversine_distance

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Address Book API",
    description="An API for managing addresses with location search.",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup():
    logger.info("Starting up API...")
    init_db()


@app.post("/addresses", response_model=AddressResponse, status_code=201)
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    """
    Create a new address entry.
    
    Provide all required address fields latitude and longitude.
    """
    logger.info(f"Creating new address: {address.street}, {address.city}")
    
    db_address = Address(**address.model_dump())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    
    logger.info(f"Address created with ID: {db_address.id}")
    return db_address


@app.get("/addresses", response_model=List[AddressResponse])
def list_addresses(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all addresses pagination.
    """
    logger.info(f"Fetching addresses (skip={skip}, limit={limit})")
    addresses = db.query(Address).offset(skip).limit(limit).all()
    return addresses


@app.get("/addresses/nearby", response_model=List[AddressResponse])
def find_nearby_addresses(
    latitude: float = Query(..., ge=-90, le=90, description="Center latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Center longitude"),
    distance_km: float = Query(..., gt=0, description="Search radius in kilometers"),
    db: Session = Depends(get_db)
):
    """
    Find all addresses within a specified distance from a given location.
    """
    logger.info(f"Searching addresses near ({latitude}, {longitude}) within {distance_km}km")
    
    all_addresses = db.query(Address).all()
    
    nearby = []
    for addr in all_addresses:
        dist = haversine_distance(latitude, longitude, addr.latitude, addr.longitude)
        if dist <= distance_km:
            nearby.append(addr)
    
    logger.info(f"Found {len(nearby)} addresses within range")
    return nearby


@app.get("/addresses/{address_id}", response_model=AddressResponse)
def get_address(address_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific address by its ID.
    """
    logger.info(f"Fetching address with ID: {address_id}")
    
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        logger.warning(f"Address not found: {address_id}")
        raise HTTPException(status_code=404, detail="Address not found")
    
    return address


@app.put("/addresses/{address_id}", response_model=AddressResponse)
def update_address(
    address_id: int,
    address_update: AddressUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing address.
    """
    logger.info(f"Updating address with ID: {address_id}")
    
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        logger.warning(f"Address not found for update: {address_id}")
        raise HTTPException(status_code=404, detail="Address not found")
    
    # Update only provided fields
    update_data = address_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(address, field, value)
    
    db.commit()
    db.refresh(address)
    
    logger.info(f"Address {address_id} updated successfully")
    return address


@app.delete("/addresses/{address_id}", status_code=204)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    """
    Delete an address by ID.
    
    Returns 204 on success.
    """
    logger.info(f"Deleting address with ID: {address_id}")
    
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        logger.warning(f"Address not found for deletion: {address_id}")
        raise HTTPException(status_code=404, detail="Address not found")
    
    db.delete(address)
    db.commit()
    
    logger.info(f"Address {address_id} deleted successfully")
    return None
