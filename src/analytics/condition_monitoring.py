from pathlib import Path

import pandas as pd


# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------

DATA_PATH = Path("data/maintenance_data.csv")

RESULTS_DIR = Path("results")

TEMPERATURE_WARNING = 80
VIBRATION_WARNING = 5

MIN_EPISODE_DURATION_HOURS = 3


# ------------------------------------------------------------------
# TEMPERATURE ALERTS
# ------------------------------------------------------------------

def detect_temperature_alerts(machine_data):

    alerts = []

    consecutive_hours = 0
    episode_start = None

    for _, row in machine_data.iterrows():

        if row["temperature_c"] > TEMPERATURE_WARNING:

            consecutive_hours += 1

            if consecutive_hours == 1:
                episode_start = row["timestamp"]

        else:

            if consecutive_hours >= MIN_EPISODE_DURATION_HOURS:

                alerts.append(
                    {
                        "machine_id": row["machine_id"],
                        "alert_type": "HIGH_TEMPERATURE",
                        "start_time": episode_start,
                        "duration_hours": consecutive_hours
                    }
                )

            consecutive_hours = 0
            episode_start = None

    if consecutive_hours >= MIN_EPISODE_DURATION_HOURS:

        alerts.append(
            {
                "machine_id": machine_data["machine_id"].iloc[0],
                "alert_type": "HIGH_TEMPERATURE",
                "start_time": episode_start,
                "duration_hours": consecutive_hours
            }
        )

    return alerts


# ------------------------------------------------------------------
# VIBRATION ALERTS
# ------------------------------------------------------------------

def detect_vibration_alerts(machine_data):

    alerts = []

    consecutive_hours = 0
    episode_start = None

    for _, row in machine_data.iterrows():

        if row["vibration_mm_s"] > VIBRATION_WARNING:

            consecutive_hours += 1

            if consecutive_hours == 1:
                episode_start = row["timestamp"]

        else:

            if consecutive_hours >= MIN_EPISODE_DURATION_HOURS:

                alerts.append(
                    {
                        "machine_id": row["machine_id"],
                        "alert_type": "HIGH_VIBRATION",
                        "start_time": episode_start,
                        "duration_hours": consecutive_hours
                    }
                )

            consecutive_hours = 0
            episode_start = None

    if consecutive_hours >= MIN_EPISODE_DURATION_HOURS:

        alerts.append(
            {
                "machine_id": machine_data["machine_id"].iloc[0],
                "alert_type": "HIGH_VIBRATION",
                "start_time": episode_start,
                "duration_hours": consecutive_hours
            }
        )

    return alerts


# ------------------------------------------------------------------
# ALERT REPORT
# ------------------------------------------------------------------

def build_alert_report(dataset):

    all_alerts = []

    for machine_id in sorted(dataset["machine_id"].unique()):

        machine_data = (
            dataset[
                dataset["machine_id"] == machine_id
            ]
            .sort_values("timestamp")
        )

        all_alerts.extend(
            detect_temperature_alerts(
                machine_data
            )
        )

        all_alerts.extend(
            detect_vibration_alerts(
                machine_data
            )
        )

    return pd.DataFrame(all_alerts)


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------

def main():

    dataset = pd.read_csv(DATA_PATH)

    alert_report = build_alert_report(
        dataset
    )

    RESULTS_DIR.mkdir(
        exist_ok=True
    )

    alert_report.to_csv(
        RESULTS_DIR / "condition_alerts.csv",
        index=False
    )

    print(
        "\nCONDITION MONITORING SUMMARY\n"
    )

    machine_summary = pd.DataFrame(
        {
            "machine_id":
            sorted(
                dataset["machine_id"].unique()
            )
        }
    )

    if not alert_report.empty:

        alert_counts = (
            alert_report.groupby("machine_id")
            .size()
            .reset_index(
                name="alert_episodes"
            )
        )

        machine_summary = machine_summary.merge(
            alert_counts,
            on="machine_id",
            how="left"
        )

    machine_summary["alert_episodes"] = (
        machine_summary["alert_episodes"]
        .fillna(0)
        .astype(int)
    )

    print(
        machine_summary.to_string(
            index=False
        )
    )

    print(
        f"\nTotal Alert Episodes: "
        f"{len(alert_report)}"
    )

    print(
        "\nDetailed alert report saved to:"
    )

    print(
        "results/condition_alerts.csv"
    )


if __name__ == "__main__":
    main()