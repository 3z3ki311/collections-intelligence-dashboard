"Functions for loading and validating dashboards data."

from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {
    "account_id",
    "pd",
    "lgd",
    "ead",
    "expected_loss",
}

def load_predictions(file_path: str | Path) -> pd.DataFrame:
    """
    Load model predictions from a csv file.

    Parameters
    --------------
    file_path:
        Location of the predictions CSV.
    Returns
    -------
    FileNotFoundError
        If the CSV file does not exist.
    ValueError
        If the CSV file does not contain the required columns.

    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist.")

    dataframe = pd.read_csv(path)

    validate_predictions(dataframe)

    return dataframe

def validate_predictions(dataframe: pd.DataFrame) -> None:
    """Confirm that the dashboard dataset contains its required columns."""
    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns in Predictions data: {missing}")

def prepare_predictions(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean numeric columns and create dashboards risk categories"""
    prepared = dataframe.copy()

    numeric_columns = [
        "pd",
        "lgd",
        "ead",
        "expected_loss",
    ]

    for column in numeric_columns:
        prepared[column] = pd.to_numeric(
            prepared[column], errors="coerce",)

    prepared = prepared.dropna(subset= numeric_columns).reset_index(drop=True)

    prepared["risk_band"] = pd.cut(
        prepared["pd"],
        bins=[-0.01, 0.20, 0.50, 0.75, 1.00],
        labels=["Low", "Moderate", "High", "Critical"],
    )
    return prepared