from pathlib import Path

import pandas as pd


# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------

HEALTH_REPORT_PATH = Path(
    "results/asset_health_report.csv"
)

RESULTS_DIR = Path("results")


def build_recommendation(row):
    """
    Generate maintenance recommendations
    from the asset health assessment.
    """

    health_status = row["health_status"]

    issues = row["detected_issues"]

    actions = row["recommended_actions"]

    if health_status == "Critical":

        return (
            "Immediate maintenance action required. "
            f"Issues identified: {issues}. "
            f"Recommended actions: {actions}."
        )

    if health_status == "Warning":

        return (
            "Maintenance planning recommended. "
            f"Issues identified: {issues}. "
            f"Recommended actions: {actions}."
        )

    return (
        "Asset operating normally. "
        "Continue routine monitoring."
    )


def main():

    health_report = pd.read_csv(
        HEALTH_REPORT_PATH
    )

    recommendations = []

    for _, row in health_report.iterrows():

        recommendations.append(
            {
                "machine_id":
                    row["machine_id"],

                "health_status":
                    row["health_status"],

                "risk_level":
                    row["risk_level"],

                "recommendation":
                    build_recommendation(
                        row
                    )
            }
        )

    recommendation_report = pd.DataFrame(
        recommendations
    )

    RESULTS_DIR.mkdir(
        exist_ok=True
    )

    output_path = (
        RESULTS_DIR
        / "maintenance_recommendations.csv"
    )

    recommendation_report.to_csv(
        output_path,
        index=False
    )

    print(
        "\nMAINTENANCE RECOMMENDATIONS\n"
    )

    summary_view = recommendation_report[
        [
            "machine_id",
            "health_status",
            "risk_level"
        ]
    ]

    print(
        summary_view.to_string(
            index=False
        )
    )

    print(
        "\nDetailed recommendations saved to:"
    )

    print(
        "results/maintenance_recommendations.csv"
    )


if __name__ == "__main__":
    main()