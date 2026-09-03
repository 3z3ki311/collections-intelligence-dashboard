"""Reusable Streamlit layout components"""

import pandas as pd
import streamlit as st

from dashboard.metrics import (
    calculate_high_risk_share,
    calculate_portfolio_metrics,
)

def render_header() -> None:
    """Render the application heading."""
    st.title("Collections Intelligence Dashboard")

    st.caption(
        "Portfolio risk, expected-loss analysis, "
        "and collections prioritization."
    )

def render_kpi_cards(
            dataframe: pd.DataFrame,
) -> None:
    """Render the dashboard's primary business KPIs."""

    metrics = calculate_portfolio_metrics(dataframe)

def render_kpi_cards(
        dataframe: pd.DataFrame,
) -> None:
    """Render the dashboard's primary business KPIs."""
    metrics = calculate_portfolio_metrics(dataframe)
    high_risk_share = calculate_high_risk_share(dataframe)

    column_1, column_2, column_3 = st.columns(3)

    column_1.metric(
    "Accounts",
    f"{metrics['account_count']:,}",
    )

    column_2.metric(
        "Total Exposure",
        f"{metrics['total_exposure']:,.0f}",
    )

    column_3.metric(
    "Total Expected Loss",
    f"{metrics['total_expected_loss']:,.0f}",
    )

    column_4, column_5, column_6 = st.columns(3)

    column_4.metric(
        "Average PD",
        f"{metrics['average_pd']:.1%}",
    )

    column_5.metric(
        "Average LGD",
        f"{metrics['average_lgd']:.1%}",
    )

    column_6.metric(
        "High-Risk Accounts",
        f"{high_risk_share:.1%}",
    )

def render_data_quality_summary(
        dataframe: pd.DataFrame,
) -> None:
    """Display a small expandable data-quality section."""
    with st.expander("Data quality summary"):
        missing_values = (
            dataframe.isna()
            .sum()
            .rename("missing_values")
            .reset_index()
            .rename(columns={"index": "column"})
        )

        st.dataframe(
            missing_values,
            use_container_width=True,
            hide_index=True,
        )