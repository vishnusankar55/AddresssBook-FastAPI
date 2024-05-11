from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from database import execute_query



app = FastAPI()


# Define Address Model
class Address(BaseModel):
    address_id: int
    street: str
    city: str
    state: str
    country: str
    coordinates: tuple
# Your FastAPI endpoints
@app.get("/address/{address_id}")
async def read_address(address_id: int):
    query = "SELECT * FROM addresses WHERE address_id=?"
    result = execute_query(query, (address_id,))
    if result:
        address_data = Address(address_id=result[0][0], street=result[0][1], city=result[0][2], state=result[0][3], country=result[0][4], coordinates=(result[0][5], result[0][6]))
        return address_data
    else:
        raise HTTPException(status_code=404, detail="Address not found")    

# Connect to SQLite Database
conn = sqlite3.connect('address_book.db')
c = conn.cursor()

# Create Address Table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS addresses
             (address_id INTEGER PRIMARY KEY, street TEXT, city TEXT, state TEXT, country TEXT, lat REAL, long REAL)''')
conn.commit()

# CRUD Operations
@app.post("/address/", response_model=Address)
def create_address(address: Address):
    with conn:
        c.execute("INSERT INTO addresses (address_id, street, city, state, country, lat, long) "
                  "VALUES (1, 'malappuram', 'pandikkad', kerala', india',0.01, 2.1)",
                  (address.address_id, address.street, address.city, address.state, address.country, address.coordinates[0], address.coordinates[1]))
    return address


@app.get("/address/", response_model=list[Address])
def read_all_addresses():
    try:
        c.execute("SELECT * FROM addresses")
        addresses = c.fetchall()
        return [{"address_id": address[0], "street": address[1], "city": address[2], "state": address[3], "country": address[4], "coordinates": (address[5], address[6])} for address in addresses]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/address/{address_id}", response_model=Address)
def read_address(address_id: int):
    c.execute("SELECT * FROM addresses WHERE address_id=?", (address_id,))
    result = c.fetchone()
    if result:
        address_data = Address(address_id=result[0], street=result[1], city=result[2], state=result[3], country=result[4], coordinates=(result[5], result[6]))
        return address_data
    else:
        raise HTTPException(status_code=404, detail="Address not found")

@app.put("/address/{address_id}", response_model=Address)
def update_address(address_id: int, address: Address):
    with conn:
        c.execute("UPDATE addresses SET street=?, city=?, state=?, country=?, lat=?, long=? WHERE address_id=?",
                  (address.street, address.city, address.state, address.country, address.coordinates[0], address.coordinates[1], address_id))
    return address

@app.delete("/address/{address_id}")
def delete_address(address_id: int):
    with conn:
        c.execute("DELETE FROM addresses WHERE address_id=?", (address_id,))
    return {"message": "Address deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
