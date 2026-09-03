# Collections-Intelligence Dashboard

An end-to-end credit risk and collections decision-support application built with Python, Strealit, SQL, and machine-learning outputs.

The dashboard converts account-level credit-risk predictions into operational portfolio insights as collection teams can identify high-risk accounts, understand expected-los exposure, and prioritize resources.

The project also includes a lightweight AI-assisted summary layer that translates validated portfolio metrics into concise business-facing insights.

---

## Project Overview

The Collections Intelligence Dashboard is the presentation and decision-support layer of a broader credit-risk machine-learning workflow.

The application consumes account-level model predictions containing:

- Probability of Default (`PD`)
- Loss Given Default (`LGD`)
- Exposure at Default (`EAD`)
- Expected Loss
- Loan Grade
- Account Status
- State
- Collections Priority Rank

The dashboard transforms these outputs into:

- Portfolio-level KPIs
- Interactive visualizations
- SQL-backed portfolio summaries
- Collections priority queues
- AI-assisted portfolio interpretations
- Exportable account-level results

---

## Business Problem

Collections teams need to determine which accounts deserve attention first.

Default probability alone does not capture the full business impact of an account.

This project uses Expected Loss as a primary decision metric:

**Expected Loss = PD × LGD × EAD**

Where:

- `PD` = Probability of Default
- `LGD` = Loss Given Default
- `EAD` = Exposure at Default

Expected Loss allows account prioritization to incorporate both default risk and financial exposure.

---

## System Architecture

```text
Processed Model Predictions
        |
        v
CSV / Processed Data
        |
        v
SQLite Database
        |
        v
SQL Query Layer
        |
        v
Python Analytics
        |
        v
Streamlit Dashboard
        |
        +----------------------+
        |                      |>?
        v                      v
Portfolio KPIs          Risk Visualizations
        |                      |
        +----------+-----------+
                   |
                   v
        Collections Priority Queue
                   |
                   v
        AI-Assisted Portfolio Summary