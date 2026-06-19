from pathlib import Path

import pandas as pd


# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------

DATA_PATH = Path("data/maintenance_data.csv")

RESULTS_DIR = Path("results")

TEMPERATURE_CRITICAL = 85
VIBRATION_CRITICAL = 7

FAILURE_EPISODE_DURATION_HOURS = 6


# ------------------------------------------------------------------
# FAILURE DETECTION
# ------------------------------------------------------------------

def count_failure_episodes(machine_df):
    """
    Count sustained failure events.

    A failure episode is recorded only when
    abnormal operating conditions persist
    for at least six consecutive hours.
    """

    abnormal_condition = (
        (machine_df["temperature_c"] > TEMPERATURE_CRITICAL)
        |
        (machine_df["vibration_mm_s"] > VIBRATION_CRITICAL)
    )

    consecutive_hours = 0
    in_failure_episode = False
    failure_count = 0

    for is_abnormal in abnormal_condition:

        if is_abnormal:

            consecutive_hours += 1

            if (
                consecutive_hours
                >= FAILURE_EPISODE_DURATION_HOURS
                and not in_failure_episode
            ):
                failure_count += 1
                in_failure_episode = True

        else:

            consecutive_hours = 0
            in_failure_episode = False

    return failure_count


# ------------------------------------------------------------------
# KPI CALCULATION
# ------------------------------------------------------------------

def calculate_machine_kpis(machine_df):
    """
    Calculate reliability and performance KPIs.
    """

    machine_df = machine_df.sort_values(
        by="timestamp"
    )

    machine_id = (
        machine_df["machine_id"]
        .iloc[0]
    )

    total_runtime_hours = (
        machine_df["runtime_hours"]
        .sum()
    )

    total_downtime_hours = (
        machine_df["downtime_minutes"]
        .sum()
        / 60
    )

    availability = (
        total_runtime_hours
        /
        (
            total_runtime_hours
            + total_downtime_hours
        )
    ) * 100

    failure_episodes = (                    #Failure Episodes measure reliability failures
        count_failure_episodes(             #while Alert Episodes measure condition-monitoring abnormalities
            machine_df                      #hence Alert Episodes may exceed Failure Episodes
        )
    )

    if failure_episodes > 0:

        mtbf = (
            total_runtime_hours
            / failure_episodes
        )

        mttr = (
            total_downtime_hours
            / failure_episodes
        )

    else:

        mtbf = total_runtime_hours
        mttr = 0

    return {
        "Machine": machine_id,
        "Availability (%)": round(
            availability,
            2
        ),
        "Failure Episodes": int(
            failure_episodes
        ),
        "MTBF (hrs)": round(
            mtbf,
            2
        ),
        "MTTR (hrs)": round(
            mttr,
            2
        ),
        "Total Downtime (hrs)": round(
            total_downtime_hours,
            2
        ),
        "Energy Consumption (kWh)": round(
            machine_df["energy_kwh"].sum(),
            2
        ),
        "Avg Temperature (°C)": round(
            machine_df["temperature_c"].mean(),
            2
        ),
        "Avg Vibration (mm/s)": round(
            machine_df["vibration_mm_s"].mean(),
            2
        )
    }


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------

def main():

    dataset = pd.read_csv(
        DATA_PATH
    )

    kpi_results = []

    for machine_id in sorted(
        dataset["machine_id"].unique()
    ):

        machine_data = dataset[
            dataset["machine_id"] == machine_id
        ]

        kpi_results.append(
            calculate_machine_kpis(
                machine_data
            )
        )

    kpi_report = pd.DataFrame(
        kpi_results
    )

    RESULTS_DIR.mkdir(
        exist_ok=True
    )

    output_path = (
        RESULTS_DIR
        / "kpi_report.csv"
    )

    kpi_report.to_csv(
        output_path,
        index=False
    )

    print(
        "\nMAINTENANCE KPI SUMMARY\n"
    )

    summary_view = kpi_report[
        [
            "Machine",
            "Availability (%)",
            "Failure Episodes"
        ]
    ]

    print(
        summary_view.to_string(
            index=False
        )
    )

    print(
        "\nDetailed KPI report saved to:"
    )

    print(
        "results/kpi_report.csv"
    )


if __name__ == "__main__":
    main()