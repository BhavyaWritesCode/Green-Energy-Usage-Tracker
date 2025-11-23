from data_operations import (
    login_user,
    register_user,
    add_energy_usage,
    fetch_energy_usage_by_user,
    month_exists
)
from analytics import get_full_analytics
from recommendation import generate_recommendations
from config import MONTHS


def login_screen():
    print("\n====== LOGIN ======")
    email = input("Email: ").strip()
    password = input("Password: ").strip()

    user = login_user(email, password)

    if user:
        print(f"\nLogin successful! Welcome {user['name']}.")
        return user
    else:
        print("\nInvalid email or password.\n")
        return None


def register_screen():
    print("\n====== REGISTER ======")
    name = input("Full Name: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    city = input("City: ").strip()

    success = register_user(name, email, password, city)

    if success:
        print("\nRegistration successful! Please login.\n")
    else:
        print("\nRegistration failed! Email may already be registered.\n")


def add_usage_screen(user_id):
    print("\n====== ADD MONTHLY USAGE ======\n")

    print("Available Months:")
    for idx, m in enumerate(MONTHS):
        print(f"{idx + 1}. {m}")

    try:
        choice = int(input("\nSelect month number: "))
        month = MONTHS[choice - 1]
    except:
        print("\nInvalid choice!")
        return

    if month_exists(user_id, month):
        print("\nYou have already entered usage for this month!")
        return

    try:
        electricity = float(input("Electricity used (kWh): "))
        water = float(input("Water used (liters): "))
        solar = float(input("Solar units generated: "))
    except:
        print("\nInvalid number entered!")
        return

    success = add_energy_usage(user_id, month, electricity, water, solar)

    if success:
        print("\nEnergy usage added successfully!\n")
    else:
        print("\nFailed to add usage!\n")


def view_analytics(user_id):
    print("\n====== ANALYTICS ======\n")
    analytics = get_full_analytics(user_id)

    print("----- Monthly Summary -----")
    for entry in analytics["monthly_summary"]:
        print(
            f"{entry['month']}: Elec={entry['electricity_kwh']} kWh, "
            f"Water={entry['water_liters']} L, Solar={entry['solar_units']} units, "
            f"Carbon={entry['carbon_footprint']} kgCO₂"
        )

    print("\n----- Averages -----")
    print(analytics["average_usage"])

    print("\n----- Extremes -----")
    print(analytics["extremes"])

    print("\n----- Month-to-Month Comparison -----")
    print(analytics["month_comparison"])


def view_recommendations(user_id):
    print("\n====== RECOMMENDATIONS ======\n")

    usage_records = fetch_energy_usage_by_user(user_id)

    if not usage_records:
        print("No usage data found! Add usage first.\n")
        return

    current = usage_records[-1]
    previous = usage_records[-2] if len(usage_records) > 1 else None

    recs = generate_recommendations(current, previous)

    print("Your personalized recommendations:\n")
    for r in recs:
        print(f"- {r}")

    print("\n")


def user_dashboard(user):
    user_id = user["user_id"]

    while True:
        print("\n====== DASHBOARD ======")
        print("1. Add Monthly Usage")
        print("2. View Analytics")
        print("3. View Recommendations")
        print("4. Logout")

        choice = input("Enter choice: ")

        if choice == '1':
            add_usage_screen(user_id)

        elif choice == '2':
            view_analytics(user_id)

        elif choice == '3':
            view_recommendations(user_id)

        elif choice == '4':
            print("\nLogging out...\n")
            break

        else:
            print("\nInvalid choice!\n")
