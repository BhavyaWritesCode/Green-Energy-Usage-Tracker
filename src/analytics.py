from data_operations import fetch_energy_usage_by_user


def get_monthly_summary(user_id):
    data = fetch_energy_usage_by_user(user_id)
    return sorted(data, key=lambda x: x["month"])


def get_average_usage(user_id):
    data = fetch_energy_usage_by_user(user_id)
    
    if not data:
        return None
    
    total_elec = sum(d["electricity_kwh"] for d in data)
    total_water = sum(d["water_liters"] for d in data)
    total_solar = sum(d["solar_units"] for d in data)
    total_carbon = sum(d["carbon_footprint"] for d in data)

    count = len(data)

    return {
        "avg_electricity": round(total_elec / count, 2),
        "avg_water": round(total_water / count, 2),
        "avg_solar": round(total_solar / count, 2),
        "avg_carbon": round(total_carbon / count, 2)
    }


def get_usage_extremes(user_id):
    data = fetch_energy_usage_by_user(user_id)

    if not data:
        return None

    highest_electricity = max(data, key=lambda x: x["electricity_kwh"])
    lowest_electricity = min(data, key=lambda x: x["electricity_kwh"])
    highest_water = max(data, key=lambda x: x["water_liters"])
    lowest_water = min(data, key=lambda x: x["water_liters"])

    return {
        "highest_electricity": {
            "month": highest_electricity["month"],
            "value": highest_electricity["electricity_kwh"]
        },
        "lowest_electricity": {
            "month": lowest_electricity["month"],
            "value": lowest_electricity["electricity_kwh"]
        },
        "highest_water": {
            "month": highest_water["month"],
            "value": highest_water["water_liters"]
        },
        "lowest_water": {
            "month": lowest_water["month"],
            "value": lowest_water["water_liters"]
        }
    }


def compare_months(user_id):
    data = get_monthly_summary(user_id)

    if len(data) < 2:
        return "Not enough data for comparison."

    comparisons = []

    for i in range(1, len(data)):
        prev = data[i - 1]
        curr = data[i]

        comparisons.append({
            "prev_month": prev["month"],
            "current_month": curr["month"],

            "electricity_change": round(curr["electricity_kwh"] - prev["electricity_kwh"], 2),
            "water_change": round(curr["water_liters"] - prev["water_liters"], 2),
            "solar_change": round(curr["solar_units"] - prev["solar_units"], 2),
            "carbon_change": round(curr["carbon_footprint"] - prev["carbon_footprint"], 2)
        })

    return comparisons


def get_full_analytics(user_id):
    return {
        "monthly_summary": get_monthly_summary(user_id),
        "average_usage": get_average_usage(user_id),
        "extremes": get_usage_extremes(user_id),
        "month_comparison": compare_months(user_id)
    }


