ELECTRICITY_FACTOR = 0.82       # kg CO2 per kWh
WATER_FACTOR = 0.00035          # kg CO2 per liter
SOLAR_REDUCTION_FACTOR = 0.82   # solar offsets electricity emissions


def calculate_carbon_footprint(electricity_kwh, water_liters, solar_units):
    """Compute carbon footprint using Indian emission factors."""

    # Ensure safe numeric values (None ➝ 0)
    try:
        electricity_kwh = float(electricity_kwh or 0)
        water_liters = float(water_liters or 0)
        solar_units = float(solar_units or 0)
    except:
        electricity_kwh = water_liters = solar_units = 0

    electricity_emissions = electricity_kwh * ELECTRICITY_FACTOR
    water_emissions = water_liters * WATER_FACTOR
    solar_offset = solar_units * SOLAR_REDUCTION_FACTOR

    carbon_footprint = electricity_emissions + water_emissions - solar_offset

    return round(max(carbon_footprint, 0), 2)
