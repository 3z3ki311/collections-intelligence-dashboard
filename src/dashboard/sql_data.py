
from pathlib import Path
import sqlite3

import pandas as pd


# ----------------------------------
# Database path
# ----------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "data" / "collections.db"

def show_columns():
    with get_connection() as conn:
        query = """
        PRAGMA table_info(collections_prioritization)
        """
        columns = pd.read_sql_query(query, conn)

    print(columns[["name", "type"]])


def get_connection():
    conn = sqlite3.connect(DB_PATH)

    tables = conn.execute("SELECT name from sqlite_master WHERE type='table';"
    ).fetchall()


    return conn
    """
    Create a connection to a SQLite database.
    """
    return sqlite3.connect(DB_PATH)

def load_all_accounts():
    """
    Load all account-level prediction data.
    """

    query = """
    SELECT *
    FROM collections_prioritization
    """

    with get_connection() as conn:
        df = pd.read_sql_query(query, conn)

    return df

def get_portfolio_summary():
    """
    Produce a simple portfolio summary grouped by risk grade.

    Change 'grade', 'expected_loss', 'loan_amnt'
    if your actual column names are different.
    """

    query = """
    SELECT 
        loan_grade,
        COUNT(*) AS account_count,
        ROUND(SUM(ead), 2) AS total_exposure,
        ROUND(AVG(expected_loss), 2) AS avg_expected_loss,
        ROUND(SUM(expected_loss), 2) AS total_expected_loss
    FROM collections_prioritization
    GROUP BY loan_grade
    ORDER BY total_expected_loss DESC   
    """

    with get_connection() as conn:
        df = pd.read_sql_query(query, conn)

    return df

def get_top_risk_accounts(limit=20):
    """
    Return accounts with the highest expected loss.
    """

    query = """
    SELECT *
    FROM collections_prioritization
    ORDER BY expected_loss DESC
    LIMIT ?
    """

    with get_connection() as conn:
        df = pd.read_sql_query(query, conn, params=(limit,))

    return df

def get_high_risk_account(min_expected_loss=1000):
    """
    Example paramterized SQL query.

    Paramerterized queries are preferable to inserting
    user values directly into SQL strings.
    """

    query = """
    SELECT *
    FROM collections_prioritization
    WHERE expected_loss >=?
    ORDER BY expected_loss DESC
    """
    with get_connection() as conn:
        df = pd.read_sql_query(query, conn, params=(min_expected_loss,))

    return df


if __name__ == "__main__":
    show_columns()


    print("\nPORTFOLIO SUMMARY")
    print(get_portfolio_summary().head())

    print("\nTOP RISK ACCOUNTS")
    print(get_top_risk_accounts().head())



