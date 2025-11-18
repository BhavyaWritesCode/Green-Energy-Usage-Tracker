
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os


load_dotenv()


def get_connection():
    """
    Creates and returns a MySQL database connection.
    Database credentials are loaded from .env.

    Returns:
        mysql.connector.connection.MySQLConnection object
    """

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        return connection

    except Error as e:
        print("Database Connection Error:", e)
        return None
