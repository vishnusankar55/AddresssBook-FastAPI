# AddresssBook-FastAPI
Set up the Environment:

Install FastAPI and SQLite.
Create a new directory for your project.
Create the SQLite Database:

Define a schema for your address book.
Create a SQLite database file (e.g., address_book.db).
Create FastAPI App:

Define your FastAPI routes and models.
Implement CRUD operations for address book entries.
Validate API Requests:

Use Pydantic models for request and response validation.
Implement validation logic in your FastAPI routes.
Save Coordinates to the Database:

Ensure that coordinates are included in the address book schema.
Store coordinates in the database when creating or updating an address entry.
Provide Terminal Commands:

Set up virtual environment (optional but recommended): python -m venv venv

Activate virtual environment: source venv/bin/activate (Linux/Mac) or venv\Scripts\activate (Windows)

Install dependencies: pip install fastapi uvicorn[standard] pydantic sqlalchemy

Run the FastAPI app: uvicorn main:app --reload

I used Postman Application to check the frontend and to check the API endpoints. Here I am adding the API endpoints

POST /address/: Create a new address.
GET /address/{address_id}: Retrieve an address by its ID.
PUT /address/{address_id}: Update an address by its ID.
DELETE /address/{address_id}: Delete an address by its ID.
GET /addresses/: Retrieve all addresses.
