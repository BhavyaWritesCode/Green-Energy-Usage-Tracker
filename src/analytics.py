from data_operations import fetch_energy_usage_by_user


def get_monthly_summary(user_id):
    data = fetch_energy_usage_by_user(user_id)
    if not data:
        return []
    return sorted(data, key=lambda x: x.get("month") or "")
    

def get_average_usage(user_id):
    data = fetch_energy_usage_by_user(user_id)
    if not data:
        return None

    def safe(v):
        return v if isinstance(v, (int, float)) else 0

    total_elec = sum(safe(d.get("electricity_kwh")) for d in data)
    total_water = sum(safe(d.get("water_liters")) for d in data)
    total_solar = sum(safe(d.get("solar_units")) for d in data)
    total_carbon = sum(safe(d.get("carbon_footprint")) for d in data)

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

    def safe(v):
        return v if isinstance(v, (int, float)) else 0

    highest_electricity = max(data, key=lambda x: safe(x.get("electricity_kwh")))
    lowest_electricity = min(data, key=lambda x: safe(x.get("electricity_kwh")))
    highest_water = max(data, key=lambda x: safe(x.get("water_liters")))
    lowest_water = min(data, key=lambda x: safe(x.get("water_liters")))

    return {
        "highest_electricity": {
            "month": highest_electricity.get("month"),
            "value": safe(highest_electricity.get("electricity_kwh"))
        },
        "lowest_electricity": {
            "month": lowest_electricity.get("month"),
            "value": safe(lowest_electricity.get("electricity_kwh"))
        },
        "highest_water": {
            "month": highest_water.get("month"),
            "value": safe(highest_water.get("water_liters"))
        },
        "lowest_water": {
            "month": lowest_water.get("month"),
            "value": safe(lowest_water.get("water_liters"))
        }
    }


def compare_months(user_id):
    data = get_monthly_summary(user_id)
    if len(data) < 2:
        return []

    def safe(v):
        return v if isinstance(v, (int, float)) else 0

    comparisons = []
    for i in range(1, len(data)):
        prev = data[i - 1]
        curr = data[i]

        comparisons.append({
            "prev_month": prev.get("month"),
            "current_month": curr.get("month"),
            "electricity_change": round(safe(curr.get("electricity_kwh")) - safe(prev.get("electricity_kwh")), 2),
            "water_change": round(safe(curr.get("water_liters")) - safe(prev.get("water_liters")), 2),
            "solar_change": round(safe(curr.get("solar_units")) - safe(prev.get("solar_units")), 2),
            "carbon_change": round(safe(curr.get("carbon_footprint")) - safe(prev.get("carbon_footprint")), 2)
        })

    return comparisons


def get_full_analytics(user_id):
    return {
        "monthly_summary": get_monthly_summary(user_id),
        "average_usage": get_average_usage(user_id),
        "extremes": get_usage_extremes(user_id),
        "month_comparison": compare_months(user_id)
    }
