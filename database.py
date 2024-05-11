import sqlite3

def get_db_connection():
    connection = sqlite3.connect("address_book.db")
    return connection

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

