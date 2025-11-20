import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

def create_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )

        if conn.is_connected():
            return conn
        else:
            print("Failed to connect to DB.")
            return None

    except Error as e:
        print("MySQL Error:", e)
        return None
