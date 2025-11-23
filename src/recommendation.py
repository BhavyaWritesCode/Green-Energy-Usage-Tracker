def generate_recommendations(current_data, previous_data=None):
    recs = []

    # Safely extract values (None → 0)
    elec = current_data.get("electricity_kwh") or 0
    water = current_data.get("water_liters") or 0
    solar = current_data.get("solar_units") or 0
    carbon = current_data.get("carbon_footprint") or 0

    # ELECTRICITY RECOMMENDATIONS
    if elec > 250:
        recs.append(
            "Your electricity usage is high. Consider using LED lighting, minimizing AC usage, "
            "cleaning AC filters, and turning off appliances when not in use."
        )

    if previous_data:
        prev_elec = previous_data.get("electricity_kwh") or 0
        if elec > prev_elec:
            recs.append(
                "Electricity usage has increased compared to last month. Review refrigerator settings, "
                "AC temperature, and check for unnecessary standby power."
            )
        else:
            recs.append("Good job! Your electricity usage decreased compared to last month.")

    # WATER USAGE RECOMMENDATIONS
    if water > 3500:
        recs.append(
            "Your water consumption is above recommended levels. Fix leaking taps, take shorter showers, "
            "and consider using low-flow faucets."
        )

    if previous_data:
        prev_water = previous_data.get("water_liters") or 0
        if water > prev_water:
            recs.append("Water usage increased this month. Try reducing wastage and check for leaks.")
        else:
            recs.append("Nice! Your water usage is lower than last month.")

    # SOLAR GENERATION RECOMMENDATIONS
    if solar < 10:
        recs.append(
            "Your solar generation is low. Clean the solar panels and ensure they are not shaded by trees or structures."
        )

    if solar > 30:
        recs.append(
            "Excellent solar energy generation! You are significantly reducing your carbon footprint."
        )

    # CARBON FOOTPRINT RECOMMENDATIONS
    if carbon > 4:
        recs.append(
            "Your carbon footprint is high. Reduce heavy electricity usage and try shifting to renewable sources."
        )
    elif carbon < 2:
        recs.append("Great job! Your carbon footprint is very low this month.")

    # FALLBACK
    if not recs:
        recs.append("Your usage is stable. Keep maintaining energy-efficient habits!")

    return recs
