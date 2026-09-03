"""Sidebar controls for filtering portfolio data."""

import pandas as pd
import streamlit as st


def render_sidebar(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Display dashboard filters and return filtered data.
    """

    st.sidebar.header("Portfolio Filters")

    filtered = dataframe.copy()

    # Loan grade filter
    if "loan_grade" in filtered.columns:
        available_grades = sorted(
            filtered["loan_grade"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_grades = st.sidebar.multiselect(
            "Loan grade",
            options=available_grades,
            default=available_grades,
        )

        if selected_grades:
            filtered = filtered[
                filtered["loan_grade"]
                .astype(str)
                .isin(selected_grades)
            ]

    # State filter
    if "state" in filtered.columns:
        available_states = sorted(
            filtered["state"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_states = st.sidebar.multiselect(
            "State",
            options=available_states,
            default=available_states,
        )

        if selected_states:
            filtered = filtered[
                filtered["state"]
                .astype(str)
                .isin(selected_states)
            ]

    # Loan status filter
    if "loan_status" in filtered.columns:
        available_statuses = sorted(
            filtered["loan_status"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_statuses = st.sidebar.multiselect(
            "Loan status",
            options=available_statuses,
            default=available_statuses,
        )

        if selected_statuses:
            filtered = filtered[
                filtered["loan_status"]
                .astype(str)
                .isin(selected_statuses)
            ]

    # Probability of default range filter
    minimum_pd, maximum_pd = st.sidebar.slider(
        "Probability of default",
        min_value=0.0,
        max_value=1.0,
        value=(0.0, 1.0),
        step=0.01,
    )

    filtered = filtered[
        filtered["pd"].between(
            minimum_pd,
            maximum_pd,
            inclusive="both",
        )
    ]

    st.sidebar.caption(
        f"{len(filtered):,} accounts selected"
    )

    return filtered.reset_index(drop=True)