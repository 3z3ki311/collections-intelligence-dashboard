"""Business and portfolio metrics used by the dashboard."""

import pandas as pd


def calculate_portfolio_metrics(
    dataframe: pd.DataFrame,
) -> dict[str, float | int]:
    """
    Calculate top-level portfolio KPIs.
    """

    if dataframe.empty:
        return {
            "account_count": 0,
            "total_exposure": 0.0,
            "total_expected_loss": 0.0,
            "average_pd": 0.0,
            "average_lgd": 0.0,
            "average_expected_loss": 0.0,
        }

    return {
        "account_count": int(len(dataframe)),
        "total_exposure": float(
            dataframe["ead"].sum()
        ),
        "total_expected_loss": float(
            dataframe["expected_loss"].sum()
        ),
        "average_pd": float(
            dataframe["pd"].mean()
        ),
        "average_lgd": float(
            dataframe["lgd"].mean()
        ),
        "average_expected_loss": float(
            dataframe["expected_loss"].mean()
        ),
    }


def calculate_high_risk_share(
    dataframe: pd.DataFrame,
    threshold: float = 0.50,
) -> float:
    """
    Calculate the share of accounts at or above
    the specified probability-of-default threshold.
    """

    if dataframe.empty:
        return 0.0

    high_risk_count = (
        dataframe["pd"] >= threshold
    ).sum()

    return float(
        high_risk_count / len(dataframe)
    )


def get_priority_accounts(
    dataframe: pd.DataFrame,
    limit: int = 20,
) -> pd.DataFrame:
    """
    Return accounts with the highest expected losses.
    """

    if dataframe.empty:
        return dataframe.copy()

    columns = [
        column
        for column in [
            "account_id",
            "borrower_name",
            "loan_grade",
            "state",
            "pd",
            "lgd",
            "ead",
            "expected_loss",
            "risk_band",
        ]
        if column in dataframe.columns
    ]

    return (
        dataframe
        .sort_values(
            "expected_loss",
            ascending=False,
        )
        .head(limit)
        .loc[:, columns]
        .reset_index(drop=True)
    )