from pathlib import Path

import pandas as pd


# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------

DATA_PATH = Path("data/maintenance_data.csv")

ALERT_PATH = Path(
    "results/condition_alerts.csv"
)

RESULTS_DIR = Path("results")

TEMPERATURE_WARNING = 80
TEMPERATURE_CRITICAL = 85

VIBRATION_WARNING = 5
VIBRATION_CRITICAL = 7

DOWNTIME_WARNING = 4500

WARNING_ALERT_EPISODES = 2
CRITICAL_ALERT_EPISODES = 5


# ------------------------------------------------------------------
# HEALTH EVALUATION
# ------------------------------------------------------------------

def evaluate_temperature(max_temperature):

    issues = []
    actions = []

    if max_temperature > TEMPERATURE_CRITICAL:

        issues.append("Overheating")
        actions.append(
            "Inspect cooling system"
        )

    elif max_temperature >= TEMPERATURE_WARNING:

        issues.append(
            "Elevated temperature"
        )

        actions.append(
            "Monitor thermal performance"
        )

    return issues, actions


def evaluate_vibration(max_vibration):

    issues = []
    actions = []

    if max_vibration > VIBRATION_CRITICAL:

        issues.append(
            "Excessive vibration"
        )

        actions.extend(
            [
                "Inspect bearings",
                "Inspect shaft alignment"
            ]
        )

    elif max_vibration >= VIBRATION_WARNING:

        issues.append(
            "Elevated vibration"
        )

        actions.append(
            "Schedule vibration inspection"
        )

    return issues, actions


def evaluate_downtime(total_downtime):

    issues = []
    actions = []

    if total_downtime > DOWNTIME_WARNING:

        issues.append(
            "Excessive downtime"
        )

        actions.append(
            "Review preventive maintenance schedule"
        )

    return issues, actions


def evaluate_alert_history(alert_count):

    issues = []
    actions = []

    if alert_count >= CRITICAL_ALERT_EPISODES:

        issues.append(
            "Frequent alert episodes"
        )

        actions.append(
            "Investigate recurring abnormal operating conditions"
        )

    elif alert_count >= WARNING_ALERT_EPISODES:

        issues.append(
            "Recurring alert episodes"
        )

        actions.append(
            "Increase condition monitoring frequency"
        )

    return issues, actions


def determine_health_status(
    max_temperature,
    max_vibration,
    total_downtime,
    alert_count
):

    if (
        max_temperature > TEMPERATURE_CRITICAL
        or max_vibration > VIBRATION_CRITICAL
        or alert_count >= CRITICAL_ALERT_EPISODES
    ):
        return "Critical", "High"

    if (
        max_temperature >= TEMPERATURE_WARNING
        or max_vibration >= VIBRATION_WARNING
        or total_downtime > DOWNTIME_WARNING
        or alert_count >= WARNING_ALERT_EPISODES
    ):
        return "Warning", "Medium"

    return "Healthy", "Low"


# ------------------------------------------------------------------
# MACHINE ASSESSMENT
# ------------------------------------------------------------------

def assess_machine_health(
    machine_data,
    alert_data
):

    machine_id = machine_data["machine_id"].iloc[0]

    max_temperature = (
        machine_data["temperature_c"].max()
    )

    max_vibration = (
        machine_data["vibration_mm_s"].max()
    )

    total_downtime = (
        machine_data["downtime_minutes"].sum()
    )

    alert_count = len(
        alert_data[
            alert_data["machine_id"]
            == machine_id
        ]
    )

    issues = []
    actions = []

    temp_issues, temp_actions = (
        evaluate_temperature(
            max_temperature
        )
    )

    vib_issues, vib_actions = (
        evaluate_vibration(
            max_vibration
        )
    )

    downtime_issues, downtime_actions = (
        evaluate_downtime(
            total_downtime
        )
    )

    alert_issues, alert_actions = (
        evaluate_alert_history(
            alert_count
        )
    )

    issues.extend(temp_issues)
    issues.extend(vib_issues)
    issues.extend(downtime_issues)
    issues.extend(alert_issues)

    actions.extend(temp_actions)
    actions.extend(vib_actions)
    actions.extend(downtime_actions)
    actions.extend(alert_actions)

    health_status, risk_level = (
        determine_health_status(
            max_temperature,
            max_vibration,
            total_downtime,
            alert_count
        )
    )

    if not issues:

        issues.append(
            "No abnormal conditions detected"
        )

    if not actions:

        actions.append(
            "Continue normal operation"
        )

    return {
        "machine_id": machine_id,
        "max_temperature_c": round(
            max_temperature,
            2
        ),
        "max_vibration_mm_s": round(
            max_vibration,
            2
        ),
        "total_downtime_min": int(
            total_downtime
        ),
        "alert_episodes": int(
            alert_count
        ),
        "health_status": health_status,
        "risk_level": risk_level,
        "detected_issues": "; ".join(
            issues
        ),
        "recommended_actions": "; ".join(
            actions
        )
    }


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------

def main():

    dataset = pd.read_csv(DATA_PATH)

    alert_report = pd.read_csv(
        ALERT_PATH
    )

    assessment_results = []

    for machine_id in sorted(
        dataset["machine_id"].unique()
    ):

        machine_data = dataset[
            dataset["machine_id"]
            == machine_id
        ]

        assessment_results.append(
            assess_machine_health(
                machine_data,
                alert_report
            )
        )

    health_report = pd.DataFrame(
        assessment_results
    )

    RESULTS_DIR.mkdir(
        exist_ok=True
    )

    health_report.to_csv(
        RESULTS_DIR / "asset_health_report.csv",
        index=False
    )

    print(
        "\nASSET HEALTH REPORT\n"
    )

    summary_view = health_report[
        [
            "machine_id",
            "health_status",
            "risk_level",
            "alert_episodes"
        ]
    ]

    print(
        summary_view.to_string(
            index=False
        )
    )

    print(
        "\nDetailed health assessment saved to:"
    )

    print(
        "results/asset_health_report.csv"
    )


if __name__ == "__main__":
    main()