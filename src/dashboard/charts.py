"""Plotly visualizations for portfolio and model outputs"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def build_pd_histogram(
        dataframe: pd.DataFrame,
    ) -> go.Figure:
    """Build a probability-of-default distribution chart."""
    figure = px.histogram(
        dataframe,
        x="pd",
        nbins=20,
        title="Probability of Default Distribution",
        labels={
            "pd": "Probability of Default",
            "count": "Accounts",
        },
    )

    figure.update_layout(
        xaxis_tickformat=".0%",
        bargap=0.05,
    )


    return figure

def build_expected_loss_by_grade(
        dataframe: pd.DataFrame,
) -> go.Figure:
    """Aggregate expected loss by loan grade."""
    if "loan_grade" not in dataframe.columns:
        return empty_figure(
            "Expected Loss by Loan Grade",
            "Loan grade is not available.",
        )

    grouped = (
        dataframe.groupby(
        "loan_grade",
            as_index=False,
            observed=True,
        )["expected_loss"]
        .sum()
        .sort_values(
            "expected_loss",
            ascending=False,
        )
    )

    figure = px.bar(
        grouped,
        x="loan_grade",
        y="expected_loss",
        title="Expected Loss by Loan Grade",
        labels={
            "loan_grade": "Loan Grade",
            "expected_loss": "Expected Loss",
        },
    )

    figure.update_layout(
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
    )

    return figure

def build_risk_band_chart(
        dataframe: pd.DataFrame,
) -> go.Figure:
    """Show the number of accounts in each risk band."""
    counts = (
        dataframe["risk_band"]
        .value_counts(sort=False)
        .rename_axis("risk_band")
        .reset_index(name="accounts")
    )

    figure = px.bar(
        counts,
        x="risk_band",
        y="accounts",
        title="Accounts by Risk Band",
        labels={
            "risk_band": "Risk Band",
            "accounts": "Number of Accounts",
        },
    )


    return figure

def build_expected_loss_by_state(
        dataframe: pd.DataFrame,
) -> go.Figure:
    """Aggregate portfolio expected loss by state."""
    if "state" not in dataframe.columns:
        return empty_figure(
            "Expected Loss by State",
            "State is not available",
        )

    grouped = (
        dataframe.groupby(
            "state",
            as_index=False,
            )["expected_loss"]
        .sum()
        .sort_values(
            "expected_loss",
            ascending=False,
        )
        .head(15)
    )

    figure = px.bar(
        grouped,
        x="state",
        y="expected_loss",
        title="Top States by Expected Loss",
        labels={
            "state": "State",
            "expected_loss": "Expected Loss",
        },
    )

    figure.update_layout(
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
    )

    return figure

def build_pd_vs_expected_loss(
        dataframe: pd.DataFrame,
) -> go.Figure:
    """Compare probability of default and expected loss."""
    hover_columns = [
        column
        for column in [
            "account_id",
            "loan_grade",
            "state",
        ]
        if column in dataframe.columns
    ]

    figure = px.scatter(
        dataframe,
        x="pd",
        y="expected_loss",
        size="ead",
        color="risk_band",
        hover_data=hover_columns,
        title="Probability of Default vs. Expected Loss",
        labels={
            "pd": "Probability of Default",
            "expected_loss": "Expected Loss",
            "ead": "Exposure at Default",
            "risk_band": "Risk Band",
        },
    )

    figure.update_layout(
        xaxis_tickformat=".0%",
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
    )

    return figure

def empty_figure(
        title: str,
        message: str,
) -> go.Figure:
    """Return an explanatory placeholder chart."""
    figure = go.Figure()

    figure.update_layout(title=title)

    figure.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
    )


    return figure
