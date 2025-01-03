import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def connect_to_db():
    """Connect to the database."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def execute_sql_query(connection, query):
    """Execute the SQL query and fetch results."""
    cursor = connection.cursor(dictionary=True)  # Return results as dict
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results
