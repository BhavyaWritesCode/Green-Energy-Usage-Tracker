import os
import matplotlib.pyplot as plt
from data_operations import fetch_energy_usage_by_user

GRAPH_DIR = "assets/graphs"
os.makedirs(GRAPH_DIR, exist_ok=True)


def _extract(records):
    months = [r.get("month") for r in records]
    electricity = [r.get("electricity_kwh") or 0 for r in records]
    water = [r.get("water_liters") or 0 for r in records]
    solar = [r.get("solar_units") or 0 for r in records]
    carbon = [r.get("carbon_footprint") or 0 for r in records]
    return months, electricity, water, solar, carbon


def _line_chart(x, y, title, ylabel, filename):
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, marker="o")
    plt.title(title)
    plt.xlabel("Month")
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    path = os.path.join(GRAPH_DIR, filename)
    plt.savefig(path)
    plt.close()
    return path


def _bar_chart(x, y, title, ylabel, filename):
    plt.figure(figsize=(10, 5))
    plt.bar(x, y)
    plt.title(title)
    plt.xlabel("Month")
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.grid(axis="y")
    plt.tight_layout()

    path = os.path.join(GRAPH_DIR, filename)
    plt.savefig(path)
    plt.close()
    return path


def _pie_chart(labels, values, title, filename):
    values = [v if v > 0 else 0.01 for v in values]

    plt.figure(figsize=(7, 7))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title(title)
    plt.tight_layout()

    path = os.path.join(GRAPH_DIR, filename)
    plt.savefig(path)
    plt.close()
    return path


def _dual_axis_chart(months, y1, y2, label1, label2, title, filename):
    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.set_xlabel("Month")
    ax1.set_ylabel(label1)
    line1 = ax1.plot(months, y1, marker="o", label=label1)

    ax2 = ax1.twinx()
    ax2.set_ylabel(label2)
    line2 = ax2.plot(months, y2, marker="s", label=label2)

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper left")

    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()

    path = os.path.join(GRAPH_DIR, filename)
    plt.savefig(path)
    plt.close()
    return path


def generate_all_visualizations(user_id):
    data = fetch_energy_usage_by_user(user_id)
    if not data:
        return None

    months, elect, water, solar, carbon = _extract(data)
    outputs = {}

    outputs["electricity_line"] = _line_chart(
        months, elect, "Electricity Usage Trend", "kWh",
        f"user_{user_id}_electricity_line.png"
    )

    outputs["water_line"] = _line_chart(
        months, water, "Water Usage Trend", "Liters",
        f"user_{user_id}_water_line.png"
    )

    outputs["solar_line"] = _line_chart(
        months, solar, "Solar Generation Trend", "Units",
        f"user_{user_id}_solar_line.png"
    )

    outputs["carbon_line"] = _line_chart(
        months, carbon, "Carbon Footprint Trend", "kg CO₂",
        f"user_{user_id}_carbon_line.png"
    )

    outputs["electricity_bar"] = _bar_chart(
        months, elect, "Electricity Usage Comparison", "kWh",
        f"user_{user_id}_electricity_bar.png"
    )

    outputs["water_bar"] = _bar_chart(
        months, water, "Water Usage Comparison", "Liters",
        f"user_{user_id}_water_bar.png"
    )

    outputs["elec_solar_dual"] = _dual_axis_chart(
        months, elect, solar,
        "Electricity (kWh)", "Solar Units",
        "Electricity vs Solar Energy",
        f"user_{user_id}_elec_vs_solar.png"
    )

    latest = data[-1]
    pie_labels = ["Electricity (kWh)", "Water (Liters/100)", "Solar Offset (Units × 0.82)"]
    pie_values = [
        latest.get("electricity_kwh") or 0,
        (latest.get("water_liters") or 0) / 100,
        (latest.get("solar_units") or 0) * 0.82
    ]

    outputs["monthly_pie"] = _pie_chart(
        pie_labels,
        pie_values,
        f"Consumption Breakdown: {latest.get('month')}",
        f"user_{user_id}_pie.png"
    )

    return outputs
