import subprocess
import sys


PIPELINE_STEPS = [
    "src/data_preparation/generate_dataset.py",
    "src/data_preparation/validate_dataset.py",
    "src/analytics/calculate_kpis.py",
    "src/analytics/condition_monitoring.py",
    "src/analytics/asset_health_assessment.py",
    "src/analytics/recommend_maintenance.py",
    "src/visualization/industrial_dashboard.py"
]


def run_step(step_number, total_steps, script_path):
    """
    Execute one pipeline step.
    """

    print("\n" + "=" * 60)

    print(
        f"STEP {step_number}/{total_steps}"
    )

    print(
        f"EXECUTING: {script_path}"
    )

    print("=" * 60)

    result = subprocess.run(
        [sys.executable, script_path]
    )

    if result.returncode != 0:

        raise RuntimeError(
            "\nPipeline execution failed.\n"
            f"Failed step: {script_path}"
        )


def print_final_summary():
    """
    Display generated project outputs.
    """

    print("\n" + "=" * 60)

    print(
        "PIPELINE COMPLETED SUCCESSFULLY"
    )

    print("=" * 60)

    print(
        "\nGenerated Reports:"
    )

    print(
        "results/kpi_report.csv"
    )

    print(
        "results/condition_alerts.csv"
    )

    print(
        "results/asset_health_report.csv"
    )

    print(
        "results/maintenance_recommendations.csv"
    )

    print(
        "\nGenerated Dashboards:"
    )

    print(
        "results/01_max_temperature.png"
    )

    print(
        "results/02_max_vibration.png"
    )

    print(
        "results/03_total_downtime.png"
    )

    print(
        "results/04_alert_count.png"
    )

    print(
        "results/05_asset_health_status.png"
    )


def main():

    print(
        "\nSME MAINTENANCE ANALYTICS PIPELINE"
    )

    print(
        "Industrial Condition Monitoring and Asset Health Assessment\n"
    )

    total_steps = len(
        PIPELINE_STEPS
    )

    for step_number, script_path in enumerate(
        PIPELINE_STEPS,
        start=1
    ):

        run_step(
            step_number,
            total_steps,
            script_path
        )

    print_final_summary()


if __name__ == "__main__":
    main()