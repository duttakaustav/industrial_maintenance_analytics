from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------

DATA_PATH = Path("data/maintenance_data.csv")

ALERT_PATH = Path(
    "results/condition_alerts.csv"
)

HEALTH_PATH = Path(
    "results/asset_health_report.csv"
)

RESULTS_DIR = Path("results")


# ------------------------------------------------------------------
# COMMON VISUAL UTILITIES
# ------------------------------------------------------------------

def apply_chart_style():

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )


def add_value_labels(
    bars,
    decimals=2
):

    for bar in bars:

        value = bar.get_height()

        plt.text(
            bar.get_x()
            + bar.get_width() / 2,
            value,
            f"{value:.{decimals}f}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold"
        )


def save_chart(filename):

    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR / filename,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ------------------------------------------------------------------
# MAXIMUM TEMPERATURE
# ------------------------------------------------------------------

def create_temperature_dashboard(dataset):

    summary = (
        dataset.groupby("machine_id")
        ["temperature_c"]
        .max()
        .reset_index()
    )

    colors = []

    for temperature in summary["temperature_c"]:

        if temperature > 85:
            colors.append("red")

        elif temperature >= 80:
            colors.append("orange")

        else:
            colors.append("green")

    plt.figure(figsize=(8, 5))

    bars = plt.bar(
        summary["machine_id"],
        summary["temperature_c"],
        color=colors
    )

    plt.axhline(
        80,
        linestyle="--",
        linewidth=2,
        label="Warning Limit (80°C)"
    )

    plt.axhline(
        85,
        linestyle=":",
        linewidth=2,
        label="Critical Limit (85°C)"
    )

    apply_chart_style()

    add_value_labels(
        bars,
        decimals=2
    )

    plt.title(
        "Maximum Recorded Temperature",
        fontsize=18,
        fontweight="bold"
    )

    plt.xlabel("Machine")
    plt.ylabel("Temperature (°C)")
    plt.legend()

    save_chart(
        "01_max_temperature.png"
    )


# ------------------------------------------------------------------
# MAXIMUM VIBRATION
# ------------------------------------------------------------------

def create_vibration_dashboard(dataset):

    summary = (
        dataset.groupby("machine_id")
        ["vibration_mm_s"]
        .max()
        .reset_index()
    )

    colors = []

    for vibration in summary["vibration_mm_s"]:

        if vibration > 7:
            colors.append("red")

        elif vibration >= 5:
            colors.append("orange")

        else:
            colors.append("green")

    plt.figure(figsize=(8, 5))

    bars = plt.bar(
        summary["machine_id"],
        summary["vibration_mm_s"],
        color=colors
    )

    plt.axhline(
        5,
        linestyle="--",
        linewidth=2,
        label="Warning Limit (5 mm/s)"
    )

    plt.axhline(
        7,
        linestyle=":",
        linewidth=2,
        label="Critical Limit (7 mm/s)"
    )

    apply_chart_style()

    add_value_labels(
        bars,
        decimals=2
    )

    plt.title(
        "Maximum Recorded Vibration",
        fontsize=18,
        fontweight="bold"
    )

    plt.xlabel("Machine")
    plt.ylabel("Vibration (mm/s)")
    plt.legend()

    save_chart(
        "02_max_vibration.png"
    )


# ------------------------------------------------------------------
# TOTAL DOWNTIME
# ------------------------------------------------------------------

def create_downtime_dashboard(dataset):

    summary = (
        dataset.groupby("machine_id")
        ["downtime_minutes"]
        .sum()
        .reset_index()
    )

    ranking = (
        summary.sort_values(
            by="downtime_minutes"
        )
    )

    color_map = {
        ranking.iloc[0]["machine_id"]:
            "green",

        ranking.iloc[1]["machine_id"]:
            "orange",

        ranking.iloc[2]["machine_id"]:
            "red"
    }

    colors = [
        color_map[machine]
        for machine in summary["machine_id"]
    ]

    plt.figure(figsize=(8, 5))

    bars = plt.bar(
        summary["machine_id"],
        summary["downtime_minutes"],
        color=colors
    )

    apply_chart_style()

    add_value_labels(
        bars,
        decimals=0
    )

    plt.title(
        "Total Downtime",
        fontsize=18,
        fontweight="bold"
    )

    plt.xlabel("Machine")
    plt.ylabel("Downtime (Minutes)")

    save_chart(
        "03_total_downtime.png"
    )


# ------------------------------------------------------------------
# ALERT EPISODES
# ------------------------------------------------------------------

def create_alert_dashboard(
    alerts,
    dataset
):

    machines = pd.DataFrame(
        {
            "machine_id":
            sorted(
                dataset["machine_id"]
                .unique()
            )
        }
    )

    summary = (
        alerts.groupby("machine_id")
        .size()
        .reset_index(
            name="alert_episodes"
        )
    )

    summary = machines.merge(
        summary,
        on="machine_id",
        how="left"
    )

    summary["alert_episodes"] = (
        summary["alert_episodes"]
        .fillna(0)
        .astype(int)
    )

    colors = []

    for episodes in summary["alert_episodes"]:

        if episodes >= 5:
            colors.append("red")

        elif episodes >= 1:
            colors.append("orange")

        else:
            colors.append("green")

    plt.figure(figsize=(8, 5))

    bars = plt.bar(
        summary["machine_id"],
        summary["alert_episodes"],
        color=colors
    )

    apply_chart_style()

    add_value_labels(
        bars,
        decimals=0
    )

    plt.title(
        "Condition Monitoring Alert Episodes",
        fontsize=18,
        fontweight="bold"
    )

    plt.xlabel("Machine")
    plt.ylabel("Alert Episodes")

    save_chart(
        "04_alert_count.png"
    )

# ------------------------------------------------------------------
# ASSET HEALTH STATUS
# ------------------------------------------------------------------

def create_health_dashboard(health_report):

    status_colors = {
        "Healthy": "green",
        "Warning": "orange",
        "Critical": "red"
    }

    status_values = {
        "Healthy": 1,
        "Warning": 2,
        "Critical": 3
    }

    colors = [
        status_colors[status]
        for status in health_report[
            "health_status"
        ]
    ]

    values = [
        status_values[status]
        for status in health_report[
            "health_status"
        ]
    ]

    plt.figure(figsize=(8, 5))

    plt.bar(
        health_report["machine_id"],
        values,
        color=colors
    )

    plt.yticks(
        [1, 2, 3],
        [
            "Healthy",
            "Warning",
            "Critical"
        ]
    )

    for index, status in enumerate(
        health_report[
            "health_status"
        ]
    ):

        plt.text(
            index,
            values[index],
            status,
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight="bold"
        )

    apply_chart_style()

    plt.title(
        "Asset Health Classification",
        fontsize=18,
        fontweight="bold"
    )

    plt.xlabel("Machine")
    plt.ylabel("Health Status")

    save_chart(
        "05_asset_health_status.png"
    )


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------

def main():

    RESULTS_DIR.mkdir(
        exist_ok=True
    )

    dataset = pd.read_csv(
        DATA_PATH
    )

    alerts = pd.read_csv(
        ALERT_PATH
    )

    health_report = pd.read_csv(
        HEALTH_PATH
    )

    create_temperature_dashboard(
        dataset
    )

    create_vibration_dashboard(
        dataset
    )

    create_downtime_dashboard(
        dataset
    )

    create_alert_dashboard(
        alerts,
        dataset
    )

    create_health_dashboard(
        health_report
    )

    print(
        "\nINDUSTRIAL DASHBOARD SUMMARY\n"
    )

    print(
        "Generated dashboard files:"
    )

    print(
        "\n01_max_temperature.png"
    )

    print(
        "02_max_vibration.png"
    )

    print(
        "03_total_downtime.png"
    )

    print(
        "04_alert_count.png"
    )

    print(
        "05_asset_health_status.png"
    )

    print(
        "\nSaved to: results/"
    )


if __name__ == "__main__":
    main()