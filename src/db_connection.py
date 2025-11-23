import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()


def create_connection():
    """Create and return a MySQL database connection."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST") or "localhost",
            user=os.getenv("DB_USER") or "root",
            password=os.getenv("DB_PASS") or "",
            database=os.getenv("DB_NAME") or ""
        )

        if conn.is_connected():
            return conn
        return None

    except Error as e:
        print("MySQL connection error:", e)
        return None
