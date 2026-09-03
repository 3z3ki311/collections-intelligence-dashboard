import sqlite3
from pathlib import Path

import pandas as pd



# -----------------------------
# File paths
# ------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CSV_PATH = (PROJECT_ROOT / "data" / "processed" / "predictions.csv")
DB_PATH = (PROJECT_ROOT / "data" / "collections.db")

def build_database():
    """
    Load the dashboard predictions CSV into a SQLite database.

    This creates/replaces a table called:
        collections_prioritization.
    """

    if not CSV_PATH.exists():
            raise FileNotFoundError(
                    f"Predictions file not found at: {CSV_PATH}"
            )

    print(f"Loading predictions from: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)
    print(f"Loaded {len(df)} rows")

    # Make sure the database folder exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:

        df.to_sql("collections_prioritization",
                  con=conn,
                  if_exists="replace",
                  index=False)

        with sqlite3.connect(DB_PATH) as conn:
            df.to_sql(
                name="collections_prioritization",
                con=conn,
                if_exists="replace",
                index=False)

            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table';"
            ).fetchall()

            print(f"Tables created: {tables}")

    print("Great, Database created successfully.")
    print(f"The Database location: {DB_PATH}")
    print("Table: collections_predictions")

if __name__ == "__main__":
    build_database()