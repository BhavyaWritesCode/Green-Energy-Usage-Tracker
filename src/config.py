

# Emission Factors (India-specific)

ELECTRICITY_EMISSION_FACTOR = 0.82        # kg CO2 per kWh
WATER_EMISSION_FACTOR = 0.00035           # kg CO2 per liter
SOLAR_OFFSET_FACTOR = 0.82                # CO2 reduction per solar unit


# Allowed Months (Dropdown / Validation)

MONTHS = [
    "January 2025", "February 2025", "March 2025",
    "April 2025", "May 2025", "June 2025",
    "July 2025", "August 2025", "September 2025",
    "October 2025", "November 2025", "December 2025"
]


# Application-level settings

APP_NAME = "Green Energy Usage Tracker"
VERSION = "1.0"
AUTHOR = "Bhavya Saini"

# Minimum & Maximum acceptable values for safety
MIN_ELECTRICITY = 0
MAX_ELECTRICITY = 2000      

MIN_WATER = 0
MAX_WATER = 20000           

MIN_SOLAR = 0
MAX_SOLAR = 500             
