# import mysql.connector

# def get_db_connection():
#     conn = mysql.connector.connect(
#         host="localhost",
#         user="root",   
#         password="root123", 
#         database="notesdb"
#     )
#     return conn
import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables (.env will be used locally only)
load_dotenv()

def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DATABASE_HOST", "localhost"),
        user=os.getenv("DATABASE_USER", "root"),
        password=os.getenv("DATABASE_PASSWORD", "root123"),
        database=os.getenv("DATABASE_NAME", "notesdb"),
        port=int(os.getenv("DATABASE_PORT", 3306))
    )
    return conn
