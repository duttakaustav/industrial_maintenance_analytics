from pathlib import Path
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------

RANDOM_SEED = 42

START_DATE = datetime(2026, 1, 1)
SIMULATION_DAYS = 90

OUTPUT_PATH = Path("data/maintenance_data.csv")


# ------------------------------------------------------------------
# MACHINE OPERATING PROFILES
# ------------------------------------------------------------------

MACHINE_PROFILES = {
    "M001": {
        "name": "CNC Machine",
        "temperature_mean": 62,
        "temperature_std": 5,
        "vibration_mean": 2.0,
        "vibration_std": 0.4,
        "energy_mean": 24,
        "energy_std": 2,
    },
    "M002": {
        "name": "Conveyor System",
        "temperature_mean": 50,
        "temperature_std": 4,
        "vibration_mean": 1.5,
        "vibration_std": 0.3,
        "energy_mean": 11,
        "energy_std": 1,
    },
    "M003": {
        "name": "Air Compressor",
        "temperature_mean": 68,
        "temperature_std": 5,
        "vibration_mean": 3.5,
        "vibration_std": 0.6,
        "energy_mean": 30,
        "energy_std": 3,
    },
}

np.random.seed(RANDOM_SEED)


# ------------------------------------------------------------------
# RECORD GENERATION
# ------------------------------------------------------------------

def generate_machine_record(
    timestamp,
    machine_id
):
    """
    Generate one hourly operating record.
    """

    profile = MACHINE_PROFILES[machine_id]

    temperature = np.random.normal(
        profile["temperature_mean"],
        profile["temperature_std"]
    )

    vibration = np.random.normal(
        profile["vibration_mean"],
        profile["vibration_std"]
    )

    energy = np.random.normal(
        profile["energy_mean"],
        profile["energy_std"]
    )

    runtime_hours = np.random.uniform(
        0.8,
        1.0
    )

    downtime_minutes = np.random.choice(
        [0, 0, 0, 0, 5, 10, 15],
        p=[
            0.60,
            0.10,
            0.10,
            0.05,
            0.08,
            0.05,
            0.02
        ]
    )

    return {
        "timestamp": timestamp,
        "machine_id": machine_id,
        "temperature_c": round(
            temperature,
            2
        ),
        "vibration_mm_s": round(
            vibration,
            2
        ),
        "runtime_hours": round(
            runtime_hours,
            2
        ),
        "downtime_minutes": downtime_minutes,
        "energy_kwh": round(
            energy,
            2
        ),
    }


# ------------------------------------------------------------------
# FAILURE INJECTION
# ------------------------------------------------------------------

def inject_failures(df):
    """
    Inject controlled degradation events.
    """

    # --------------------------------------------------------------
    # M003 AIR COMPRESSOR
    # Bearing degradation event
    # --------------------------------------------------------------

    compressor_mask = (
        (df["machine_id"] == "M003")
        & (df["timestamp"] >= "2026-02-15")
        & (df["timestamp"] <= "2026-02-22")
    )

    compressor_indices = (
        df.loc[compressor_mask].index
    )

    event_length = len(
        compressor_indices
    )

    temperature_trend = np.linspace(
        4,
        18,
        event_length
    )

    vibration_trend = np.linspace(
        1,
        5,
        event_length
    )

    df.loc[
        compressor_indices,
        "temperature_c"
    ] += temperature_trend

    df.loc[
        compressor_indices,
        "vibration_mm_s"
    ] += vibration_trend

    # --------------------------------------------------------------
    # M001 CNC MACHINE
    # Cooling system degradation
    # --------------------------------------------------------------

    cnc_mask = (
        (df["machine_id"] == "M001")
        & (df["timestamp"] >= "2026-03-10")
        & (df["timestamp"] <= "2026-03-15")
    )

    cnc_indices = (
        df.loc[cnc_mask].index
    )

    event_length = len(
        cnc_indices
    )

    temperature_trend = np.linspace(
        3,
        12,
        event_length
    )

    energy_trend = np.linspace(
        1,
        6,
        event_length
    )

    df.loc[
        cnc_indices,
        "temperature_c"
    ] += temperature_trend

    df.loc[
        cnc_indices,
        "energy_kwh"
    ] += energy_trend

    # --------------------------------------------------------------
    # M002 CONVEYOR SYSTEM
    # Mechanical misalignment event
    # --------------------------------------------------------------

    conveyor_mask = (
        (df["machine_id"] == "M002")
        & (df["timestamp"] >= "2026-03-25")
        & (df["timestamp"] <= "2026-03-30")
    )

    conveyor_indices = (
        df.loc[conveyor_mask].index
    )

    event_length = len(
        conveyor_indices
    )

    vibration_trend = np.linspace(
        0.5,
        3.0,
        event_length
    )

    downtime_trend = np.linspace(
        5,
        30,
        event_length
    )

    df.loc[
        conveyor_indices,
        "vibration_mm_s"
    ] += vibration_trend

    df.loc[
        conveyor_indices,
        "downtime_minutes"
    ] += downtime_trend.astype(
        int
    )

    return df


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------

def main():

    total_hours = (
        SIMULATION_DAYS * 24
    )

    records = []

    for hour in range(
        total_hours
    ):

        timestamp = (
            START_DATE
            + timedelta(hours=hour)
        )

        for machine_id in MACHINE_PROFILES:

            records.append(
                generate_machine_record(
                    timestamp,
                    machine_id
                )
            )

    dataset = pd.DataFrame(
        records
    )

    dataset = inject_failures(
        dataset
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    dataset.to_csv(
        OUTPUT_PATH,
        index=False
    )

    expected_records = (
        len(MACHINE_PROFILES)
        * total_hours
    )

    print(
        "\nDATASET GENERATION SUMMARY\n"
    )

    print(
        f"Random Seed: {RANDOM_SEED}"
    )

    print(
        f"\nSimulation Period: "
        f"{SIMULATION_DAYS} Days"
    )

    print(
        "Sampling Interval: 1 Hour"
    )

    print(
        f"\nMachines: "
        f"{len(MACHINE_PROFILES)}"
    )

    print(
        f"Expected Records: "
        f"{expected_records}"
    )

    print(
        f"Generated Records: "
        f"{len(dataset)}"
    )

    print(
        "\nMachine Profiles:"
    )

    for machine_id, profile in MACHINE_PROFILES.items():

        print(
            f"{machine_id} - "
            f"{profile['name']}"
        )

    print(
        "\nDataset Status: GENERATED"
    )

    print(
        f"\nDataset created: "
        f"{OUTPUT_PATH}"
    )

    print(
        f"Rows: {len(dataset)}"
    )


if __name__ == "__main__":
    main()