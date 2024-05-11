import sqlite3

# Define a function to create a new SQLite connection
def get_db_connection():
    connection = sqlite3.connect("address_book.db")
    return connection

# Define a function to execute SQL queries
def execute_query(query, params=None):
    connection = get_db_connection()
    cursor = connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result

# Your FastAPI endpoint
