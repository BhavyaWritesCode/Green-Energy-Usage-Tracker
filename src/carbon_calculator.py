"""
Indian emission factors:
- Electricity: 0.82 kg CO₂ per kWh
- Water supply & treatment: 0.00035 kg CO₂ per liter
- Solar energy: reduces carbon footprint completely (renewable)
"""

# Emission factors (India-specific)
ELECTRICITY_FACTOR = 0.82          # kg CO2 per kWh
WATER_FACTOR = 0.00035             # kg CO2 per liter
SOLAR_REDUCTION_FACTOR = 0.82      # solar offsets electricity emissions


def calculate_carbon_footprint(electricity_kwh, water_liters, solar_units):
    """
    Calculates carbon footprint using Indian emission standards.

    Returns:
        float: final carbon footprint (rounded to 2 decimals)
    """

    electricity_emissions = electricity_kwh * ELECTRICITY_FACTOR
    water_emissions = water_liters * WATER_FACTOR
    solar_offset = solar_units * SOLAR_REDUCTION_FACTOR

    carbon_footprint = electricity_emissions + water_emissions - solar_offset

    # Avoid negative outputs
    return round(max(carbon_footprint, 0), 2)
