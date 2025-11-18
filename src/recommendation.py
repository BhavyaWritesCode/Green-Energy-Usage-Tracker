def generate_recommendations(current_data, previous_data=None):

    recs = []

    elec = current_data["electricity_kwh"]
    water = current_data["water_liters"]
    solar = current_data["solar_units"]
    carbon = current_data["carbon_footprint"]

    # Electricity-based recommendations
    if elec > 250:
        recs.append(
            "Your electricity usage is high. Consider using LED lighting, minimizing AC usage, "
            "cleaning AC filters, and turning off appliances when not in use."
        )

    if previous_data:
        if elec > previous_data["electricity_kwh"]:
            recs.append(
                "Electricity usage has increased compared to last month. Review refrigerator settings, "
                "AC temperature, and check for unnecessary standby power."
            )
        else:
            recs.append(
                "Good job! Your electricity usage decreased compared to last month."
            )

    # Water usage recommendations
    if water > 3500:
        recs.append(
            "Your water consumption is above recommended levels. Fix leaking taps, take shorter showers, "
            "and consider using low-flow faucets."
        )

    if previous_data:
        if water > previous_data["water_liters"]:
            recs.append(
                "Water usage increased this month. Try reducing wastage and check for leaks."
            )
        else:
            recs.append(
                "Nice! Your water usage is lower than last month."
            )

    # Solar generation recommendations
    if solar < 10:
        recs.append(
            "Your solar generation is low. Clean the solar panels and ensure they are not shaded by trees or structures."
        )

    if solar > 30:
        recs.append(
            "Excellent solar energy generation! You are significantly reducing your carbon footprint."
        )

    # Carbon footprint recommendations
    
    if carbon > 4:
        recs.append(
            "Your carbon footprint is high. Reduce heavy electricity usage and try shifting to renewable sources."
        )
    elif carbon < 2:
        recs.append(
            "Great job! Your carbon footprint is very low this month."
        )

    # If no recommendations generated:
    if not recs:
        recs.append("Your usage is stable. Keep maintaining energy-efficient habits!")

    return recs
