from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Address(BaseModel):
    address_id: int
    street: str
    city: str
    state: str
    country: str
    coordinates: tuple

@app.post("/address/", response_model=Address)
def create_address(address: Address):
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO addresses (address_id, street, city, state, country, lat, long) "
                  "VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (address.address_id, address.street, address.city, address.state, address.country, address.coordinates[0], address.coordinates[1]))
    return address

@app.get("/address/{address_id}", response_model=Address)
def read_address(address_id: int):
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    c.execute("SELECT * FROM addresses WHERE address_id=?", (address_id,))
    result = c.fetchone()
    if result:
        address_data = Address(address_id=result[0], street=result[1], city=result[2], state=result[3], country=result[4], coordinates=(result[5], result[6]))
        return address_data
    else:
        raise HTTPException(status_code=404, detail="Address not found")

@app.put("/address/{address_id}", response_model=Address)
def update_address(address_id: int, address: Address):
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    with conn:
        c.execute("UPDATE addresses SET street=?, city=?, state=?, country=?, lat=?, long=? WHERE address_id=?",
                  (address.street, address.city, address.state, address.country, address.coordinates[0], address.coordinates[1], address_id))
    return address

@app.delete("/address/{address_id}")
def delete_address(address_id: int):
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    with conn:
        c.execute("DELETE FROM addresses WHERE address_id=?", (address_id,))
    return {"message": "Address deleted successfully"}

@app.get("/addresses/", response_model=list[Address])
def read_all_addresses():
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM addresses")
        addresses = c.fetchall()
        return [{"address_id": address[0], "street": address[1], "city": address[2], "state": address[3], "country": address[4], "coordinates": (address[5], address[6])} for address in addresses]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
