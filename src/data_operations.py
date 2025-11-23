from db_connection import create_connection
import mysql.connector
from carbon_calculator import calculate_carbon_footprint


def register_user(name, email, password, city):
    try:
        conn = create_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        query = """
            INSERT INTO users (name, email, password, city)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, email, password, city))
        conn.commit()
        return True

    except mysql.connector.Error as err:
        print("Error registering user:", err)
        return False

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def login_user(email, password):
    try:
        conn = create_connection()
        if conn is None:
            return None

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE email=%s AND password=%s"
        cursor.execute(query, (email, password))
        return cursor.fetchone()

    except mysql.connector.Error as err:
        print("Login error:", err)
        return None

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def month_exists(user_id, month):
    try:
        conn = create_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        query = """
            SELECT COUNT(*) FROM energy_usage
            WHERE user_id=%s AND month=%s
        """
        cursor.execute(query, (user_id, month))
        (count,) = cursor.fetchone()
        return count > 0

    except mysql.connector.Error as err:
        print("Error checking month:", err)
        return False

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def add_energy_usage(user_id, month, electricity, water, solar):
    try:
        conn = create_connection()
        if conn is None:
            return False

        cursor = conn.cursor()

        # Ensure that calculator never breaks even if values are None
        try:
            carbon = calculate_carbon_footprint(electricity, water, solar)
        except:
            carbon = 0

        query = """
            INSERT INTO energy_usage
            (user_id, month, electricity_kwh, water_liters, solar_units, carbon_footprint)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (user_id, month, electricity, water, solar, carbon))
        conn.commit()
        return True

    except mysql.connector.Error as err:
        print("Error adding usage:", err)
        return False

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def fetch_energy_usage_by_user(user_id):
    try:
        conn = create_connection()
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT record_id, month, electricity_kwh, water_liters,
                   solar_units, carbon_footprint
            FROM energy_usage
            WHERE user_id = %s
            ORDER BY record_id ASC
        """
        cursor.execute(query, (user_id,))
        records = cursor.fetchall()

        # Ensure no None values break analytics/recommendations
        for row in records:
            for key in row:
                if row[key] is None:
                    row[key] = 0

        return records

    except mysql.connector.Error as err:
        print("Error fetching usage:", err)
        return []

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
