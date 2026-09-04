"""Main Streamlit application entry point."""
import sys
from pathlib import Path

import streamlit as st


# Make src/ available for package imports when Streamlit runs this file.
SRC_DIR = Path(__file__).resolve().parents[1]

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0,str(SRC_DIR))

from dashboard.ai_summary import generate_portfolio_summary

from dashboard.charts import (
    build_expected_loss_by_grade,
    build_expected_loss_by_state,
    build_pd_histogram,
    build_pd_vs_expected_loss,
    build_risk_band_chart,
)
from dashboard.data_loader import (
    load_predictions,
    prepare_predictions,
)
from dashboard.layout import (
    render_data_quality_summary,
    render_header,
    render_kpi_cards,
)
from dashboard.metrics import get_priority_accounts
from dashboard.sidebar import render_sidebar
from dashboard.utils import load_yaml_config
from dashboard.sql_data import (
    get_portfolio_summary,
    get_top_risk_accounts,
)


# app.py is inside:
# project_root/src/dashboard/app.py
PROJECT_ROOT = Path(__file__).resolve().parents[2]

CONFIG_PATH = (
    PROJECT_ROOT
    / "configs"
    / "dashboard.yaml"
)


def main() -> None:
    """Run the collections intelligence dashboard."""

    # Load dashboard settings from the YAML file.
    config = load_yaml_config(CONFIG_PATH)

    app_config = config.get("app", {})

    st.set_page_config(
        page_title=app_config.get(
            "title",
            "Collections Intelligence Dashboard",
        ),
        page_icon=app_config.get(
            "page_icon",
            "📊",
        ),
        layout=app_config.get(
            "layout",
            "wide",
        ),
    )

    render_header()

    # Read the predictions path from the YAML configuration.
    relative_data_path = config.get(
        "data",
        {},
    ).get(
        "predictions_path",
        "data/processed/predictions.csv",
    )

    predictions_path = (
        PROJECT_ROOT
        / relative_data_path
    )

    # Load and prepare the account-level model predictions.
    try:
        predictions = load_predictions(
            predictions_path
        )

        predictions = prepare_predictions(
            predictions
        )

    except (FileNotFoundError, ValueError) as error:
        st.error(str(error))

        st.info(
            "Add a valid predictions.csv file to "
            "data/processed and restart the dashboard."
        )

        st.stop()

    # Apply the user's sidebar filter selections.
    filtered_predictions = render_sidebar(
        predictions
    )

    # Stop the dashboard if no accounts match the filters.
    if filtered_predictions.empty:
        st.warning(
            "No accounts match the selected filters."
        )

        st.stop()

    # Display the primary portfolio-level business metrics.
    render_kpi_cards(
        filtered_predictions
    )
    st.subheader("SQL Portfolio Summary")

    portfolio_summary = get_portfolio_summary()

    st.dataframe(
        portfolio_summary,
        width="stretch",
        hide_index=True,)
    st.subheader("AI Portfolio Summary")

    total_accounts = int(portfolio_summary["account_count"].sum())
    total_exposure = float(portfolio_summary["total_exposure"].sum())
    total_expected_loss = float(
        portfolio_summary["total_expected_loss"].sum()
    )

    highest_expected_loss_grade = str(
        portfolio_summary.iloc[0]["loan_grade"]
    )

    top_state = str(
        filtered_predictions["state"]
        .value_counts()
        .idxmax()
    )

    ai_summary = generate_portfolio_summary(
        total_accounts=total_accounts,
        total_exposure=total_exposure,
        total_expected_loss=total_expected_loss,
        highest_risk_grade=highest_expected_loss_grade,
        top_state=top_state,
    )

    st.markdown(ai_summary)

    st.divider()

    # First chart row.
    chart_column_1, chart_column_2 = st.columns(2)

    with chart_column_1:
        st.plotly_chart(
            build_pd_histogram(
                filtered_predictions
            ),
            width="stretch",
        )

    with chart_column_2:
        st.plotly_chart(
            build_expected_loss_by_grade(
                filtered_predictions
            ),
            width="stretch",
        )

    # Second chart row.
    chart_column_3, chart_column_4 = st.columns(2)

    with chart_column_3:
        st.plotly_chart(
            build_risk_band_chart(
                filtered_predictions
            ),
            width="stretch",
        )

    with chart_column_4:
        st.plotly_chart(
            build_expected_loss_by_state(
                filtered_predictions
            ),
            width="stretch",
        )

    # Full-width relationship chart.
    st.plotly_chart(
        build_pd_vs_expected_loss(
            filtered_predictions
        ),
        width="stretch",
    )

    st.divider()

    st.subheader(
        "Collections Priority Queue"
    )

    priority_accounts = get_priority_accounts(
        filtered_predictions,
        limit=20,
    )

    # Create a display copy so PD and LGD appear as percentages.
    display_priority_accounts = (
        priority_accounts.copy()
    )

    if "pd" in display_priority_accounts.columns:
        display_priority_accounts["pd"] = (
            display_priority_accounts["pd"]
            * 100
        )

    if "lgd" in display_priority_accounts.columns:
        display_priority_accounts["lgd"] = (
            display_priority_accounts["lgd"]
            * 100
        )

    st.dataframe(
        display_priority_accounts,
        width="stretch",
        hide_index=True,
        column_config={
            "pd": st.column_config.NumberColumn(
                "PD",
                format="%.1f%%",
            ),
            "lgd": st.column_config.NumberColumn(
                "LGD",
                format="%.1f%%",
            ),
            "ead": st.column_config.NumberColumn(
                "EAD",
                format="$%.2f",
            ),
            "expected_loss": (
                st.column_config.NumberColumn(
                    "Expected Loss",
                    format="$%.2f",
                )
            ),
        },
    )

    # Export the original values rather than the display-adjusted copy.
    export_data = priority_accounts.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Export priority accounts",
        data=export_data,
        file_name=(
            "collections_priority_accounts.csv"
        ),
        mime="text/csv",
    )

    render_data_quality_summary(
        filtered_predictions
    )


if __name__ == "__main__":
    main()