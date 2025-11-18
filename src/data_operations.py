import mysql.connector
from db_connection import get_connection
from carbon_calculator import calculate_carbon_footprint


# 1. USER OPERATIONS

def register_user(name, email, password, city):
    """
    Registers a new user into the users table.
    Returns True if successful, False otherwise.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO users (name, email, password, city)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, email, password, city))
        conn.commit()

        return True

    except mysql.connector.Error as err:
        print("Error during registration:", err)
        return False

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def login_user(email, password):
    """
    Validates login by checking email + password.
    Returns user record as dict on success, None on failure.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT * FROM users 
            WHERE email = %s AND password = %s
        """
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        return user  # returns dict or None

    except mysql.connector.Error as err:
        print("Login error:", err)
        return None

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# 2. ENERGY USAGE OPERATIONS

def add_energy_usage(user_id, month, electricity_kwh, water_liters, solar_units):
    """
    Inserts a new monthly usage entry for the given user.
    Automatically calculates carbon footprint.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Calculate carbon dynamically
        carbon_fp = calculate_carbon_footprint(electricity_kwh, water_liters, solar_units)

        query = """
            INSERT INTO energy_usage 
            (user_id, month, electricity_kwh, water_liters, solar_units, carbon_footprint)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (user_id, month, electricity_kwh, water_liters, solar_units, carbon_fp)

        cursor.execute(query, values)
        conn.commit()

        return True

    except mysql.connector.Error as err:
        print("Error adding usage:", err)
        return False

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# 3. FETCH USAGE FOR ANALYTICS / VISUALIZATION

def fetch_energy_usage_by_user(user_id):
    """
    Returns all energy usage records for a specific user.
    Output format: list of dictionaries.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT month, electricity_kwh, water_liters, 
                   solar_units, carbon_footprint 
            FROM energy_usage
            WHERE user_id = %s
            ORDER BY created_at ASC
        """

        cursor.execute(query, (user_id,))
        records = cursor.fetchall()

        return records  # list of dicts

    except mysql.connector.Error as err:
        print("Error fetching usage:", err)
        return []

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# 4. CHECK IF MONTH ALREADY EXISTS (prevent duplicates)


def month_exists(user_id, month):
    """
    Checks if a user already added usage for the given month.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT COUNT(*) FROM energy_usage 
            WHERE user_id = %s AND month = %s
        """

        cursor.execute(query, (user_id, month))
        (count,) = cursor.fetchone()

        return count > 0

    except mysql.connector.Error as err:
        print("Error checking month:", err)
        return False

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
