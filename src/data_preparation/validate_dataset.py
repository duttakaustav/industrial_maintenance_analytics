from pathlib import Path

import pandas as pd


# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------

DATA_PATH = Path("data/maintenance_data.csv")

VALID_MACHINES = {
    "M001",
    "M002",
    "M003"
}

EXPECTED_RECORDS_PER_MACHINE = 2160

TEMPERATURE_LIMITS = (0, 150)
VIBRATION_LIMITS = (0, 20)
RUNTIME_LIMITS = (0, 1)
DOWNTIME_LIMITS = (0, 60)
ENERGY_LIMITS = (0, 100)


# ------------------------------------------------------------------
# VALIDATION FUNCTIONS
# ------------------------------------------------------------------

def validate_missing_values(df):
    """Ensure the dataset contains no missing values."""

    missing_counts = df.isnull().sum()

    if missing_counts.sum() > 0:
        raise ValueError(
            f"Missing values detected:\n{missing_counts}"
        )


def validate_machine_ids(df):
    """Ensure only approved machine IDs exist."""

    detected_machines = set(
        df["machine_id"].unique()
    )

    invalid_machines = (
        detected_machines - VALID_MACHINES
    )

    if invalid_machines:
        raise ValueError(
            f"Invalid machine IDs detected: {invalid_machines}"
        )


def validate_machine_completeness(df):
    """
    Ensure each machine contains the expected
    number of operating records.
    """

    machine_counts = (
        df["machine_id"]
        .value_counts()
    )

    for machine_id in VALID_MACHINES:

        actual_count = machine_counts.get(
            machine_id,
            0
        )

        if actual_count != EXPECTED_RECORDS_PER_MACHINE:

            raise ValueError(
                f"{machine_id} contains "
                f"{actual_count} records. "
                f"Expected "
                f"{EXPECTED_RECORDS_PER_MACHINE}."
            )


def validate_duplicate_records(df):
    """Ensure duplicate records do not exist."""

    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:

        raise ValueError(
            f"Duplicate rows detected: "
            f"{duplicate_count}"
        )


def validate_timestamps(df):
    """Ensure timestamps are valid."""

    timestamps = pd.to_datetime(
        df["timestamp"]
    )

    if timestamps.isnull().any():

        raise ValueError(
            "Invalid timestamp values detected."
        )

    if timestamps.min() >= timestamps.max():

        raise ValueError(
            "Timestamp range is invalid."
        )


def validate_timestamp_continuity(df):
    """
    Ensure timestamps progress
    continuously in one-hour intervals.
    """

    timestamps = sorted(
        pd.to_datetime(
            df["timestamp"]
        ).unique()
    )

    for index in range(
        1,
        len(timestamps)
    ):

        time_difference = (
            timestamps[index]
            - timestamps[index - 1]
        )

        if (
            time_difference.total_seconds()
            != 3600
        ):

            raise ValueError(
                "Timestamp continuity check failed."
            )


def validate_numeric_range(
    df,
    column_name,
    minimum,
    maximum
):
    """Validate numeric operating limits."""

    invalid_rows = df[
        (df[column_name] < minimum)
        | (df[column_name] > maximum)
    ]

    if not invalid_rows.empty:

        raise ValueError(
            f"{column_name} out of range: "
            f"{len(invalid_rows)} records"
        )


# ------------------------------------------------------------------
# REPORTING
# ------------------------------------------------------------------

def print_summary(df):
    """Display dataset certification summary."""

    print(
        "\nDATASET CERTIFICATION\n"
    )

    print(
        "Status: CERTIFIED"
    )

    print(
        f"\nRows: {len(df)}"
    )

    print(
        f"Machines: "
        f"{df['machine_id'].nunique()}"
    )

    print(
        "\nDate Range:"
    )

    print(
        df["timestamp"].min()
    )

    print(
        "to"
    )

    print(
        df["timestamp"].max()
    )

    print(
        "\nMachine Distribution:"
    )

    print(
        df["machine_id"]
        .value_counts()
        .sort_index()
        .to_string()
    )


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------

def main():

    print(
        "\nSTARTING DATASET VALIDATION\n"
    )

    dataset = pd.read_csv(
        DATA_PATH
    )

    validate_missing_values(
        dataset
    )

    validate_machine_ids(
        dataset
    )

    validate_machine_completeness(
        dataset
    )

    validate_duplicate_records(
        dataset
    )

    validate_timestamps(
        dataset
    )

    validate_timestamp_continuity(
        dataset
    )

    validate_numeric_range(
        dataset,
        "temperature_c",
        *TEMPERATURE_LIMITS
    )

    validate_numeric_range(
        dataset,
        "vibration_mm_s",
        *VIBRATION_LIMITS
    )

    validate_numeric_range(
        dataset,
        "runtime_hours",
        *RUNTIME_LIMITS
    )

    validate_numeric_range(
        dataset,
        "downtime_minutes",
        *DOWNTIME_LIMITS
    )

    validate_numeric_range(
        dataset,
        "energy_kwh",
        *ENERGY_LIMITS
    )

    print(
        "\nValidation Checks Passed: 10/10"
    )

    print_summary(
        dataset
    )


if __name__ == "__main__":
    main()