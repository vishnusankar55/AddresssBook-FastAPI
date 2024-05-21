from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Tuple
import sqlite3
import math

app = FastAPI()

class Address(BaseModel):
    address_id: int
    street: str
    city: str
    state: str
    country: str
    coordinates: Tuple[float, float]

# Database connection
def get_db_connection():
    conn = sqlite3.connect('address_book.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.on_event("startup")
def startup():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS addresses
                 (address_id INTEGER PRIMARY KEY, street TEXT, city TEXT, state TEXT, country TEXT, lat REAL, long REAL)''')
    conn.commit()
    conn.close()

@app.post("/address/", response_model=Address)
def create_address(address: Address):
    conn = get_db_connection()
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO addresses (address_id, street, city, state, country, lat, long) "
                  "VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (address.address_id, address.street, address.city, address.state, address.country, address.coordinates[0], address.coordinates[1]))
    return address

@app.get("/address/{address_id}", response_model=Address)
def read_address(address_id: int):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM addresses WHERE address_id=?", (address_id,))
    result = c.fetchone()
    if result:
        address_data = Address(address_id=result['address_id'], street=result['street'], city=result['city'], state=result['state'], country=result['country'], coordinates=(result['lat'], result['long']))
        return address_data
    else:
        raise HTTPException(status_code=404, detail="Address not found")

@app.put("/address/{address_id}", response_model=Address)
def update_address(address_id: int, address: Address):
    conn = get_db_connection()
    c = conn.cursor()
    with conn:
        c.execute("UPDATE addresses SET street=?, city=?, state=?, country=?, lat=?, long=? WHERE address_id=?",
                  (address.street, address.city, address.state, address.country, address.coordinates[0], address.coordinates[1], address_id))
    return address

@app.delete("/address/{address_id}")
def delete_address(address_id: int):
    conn = get_db_connection()
    c = conn.cursor()
    with conn:
        c.execute("DELETE FROM addresses WHERE address_id=?", (address_id,))
    return {"message": "Address deleted successfully"}

@app.get("/addresses/", response_model=List[Address])
def read_all_addresses():
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM addresses")
        addresses = c.fetchall()
        return [Address(address_id=address['address_id'], street=address['street'], city=address['city'], state=address['state'], country=address['country'], coordinates=(address['lat'], address['long'])) for address in addresses]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/addresses/nearby", response_model=List[Address])
def get_addresses_nearby(lat: float, long: float, distance: float):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM addresses")
        addresses = c.fetchall()
        nearby_addresses = []

        for address in addresses:
            address_lat = address['lat']
            address_long = address['long']
            if haversine(lat, long, address_lat, address_long) <= distance:
                nearby_addresses.append(Address(address_id=address['address_id'], street=address['street'], city=address['city'], state=address['state'], country=address['country'], coordinates=(address['lat'], address['long'])))
        
        return nearby_addresses
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
