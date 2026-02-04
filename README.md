# Address Book API

A simple REST API for managing addresses with geographic coordinate support and location-based search.

## Features

- Create, read, update, and delete addresses
- Store geographic coordinates (latitude/longitude) with each address
- Search for addresses within a specified distance from a location
- Input validation using Pydantic
- SQLite database for data persistence
- Interactive API documentation via Swagger UI

## Requirements

- Python 3.8+
- pip (Python package manager)

## Setup

1. **Navigate to the project directory:**
   ```bash
   cd address-booking-app
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Documentation

Once the server is running, open your browser and go to:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/addresses` | Create a new address |
| GET | `/addresses` | List all addresses (with pagination) |
| GET | `/addresses/{id}` | Get a specific address |
| PUT | `/addresses/{id}` | Update an address |
| DELETE | `/addresses/{id}` | Delete an address |
| GET | `/addresses/nearby` | Find addresses within a distance |

## Example Usage

### Create an address:

```bash
curl -X POST "http://127.0.0.1:8000/addresses" \
  -H "Content-Type: application/json" \
  -d '{
    "street": "123 Main Street",
    "city": "New York",
    "state": "NY",
    "country": "USA",
    "postal_code": "10001",
    "latitude": 40.7128,
    "longitude": -74.0060
  }'
```

### Find nearby addresses:

```bash
curl "http://127.0.0.1:8000/addresses/nearby?latitude=40.7128&longitude=-74.0060&distance_km=10"
```

## Project Structure

```
address-booking-app/
├── app/
│   ├── __init__.py      # Package marker
│   ├── main.py          # FastAPI app and routes
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic validation schemas
│   ├── database.py      # Database setup
│   └── utils.py         # Helper functions
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Notes

- The SQLite database file (`addresses.db`) is created automatically on first run
- Coordinates are validated to be within valid ranges (-90 to 90 for latitude, -180 to 180 for longitude)
- The nearby search uses the Haversine formula for accurate distance calculations
