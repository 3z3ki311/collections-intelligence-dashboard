"""Thin AI summary layer for the dashboard."""

import os

from openai import OpenAI


def generate_fallback_summary(
    total_accounts: int,
    total_exposure: float,
    total_expected_loss: float,
    highest_risk_grade: str,
    top_state: str,
) -> str:
    """
    Generate a deterministic summary when no API key is available.
    """

    return (
        f"• Portfolio contains {total_accounts:,} accounts with "
        f"${total_exposure:,.2f} in total exposure.\n\n"
        f"• Total expected loss is ${total_expected_loss:,.2f}, "
        f"with grade {highest_risk_grade} contributing the "
        f"highest total expected loss.\n\n"
        f"• Collections teams should prioritize higher-risk "
        f"accounts and closely monitor exposure in {top_state}."
    )


def generate_portfolio_summary(
    total_accounts: int,
    total_exposure: float,
    total_expected_loss: float,
    highest_risk_grade: str,
    top_state: str,
) -> str:
    """
    Generate an LLM summary when an API key is available.

    If no API key exists, return a deterministic fallback summary.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return generate_fallback_summary(
            total_accounts=total_accounts,
            total_exposure=total_exposure,
            total_expected_loss=total_expected_loss,
            highest_risk_grade=highest_risk_grade,
            top_state=top_state,
        )

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are assisting a credit-risk collections team.

Summarize these validated portfolio metrics for a business audience.

Total accounts: {total_accounts}
Total exposure at default: ${total_exposure:,.2f}
Total expected loss: ${total_expected_loss:,.2f}
Loan grade with highest total expected loss: {highest_risk_grade}
Highest-risk state: {top_state}

Requirements:
- Use only the supplied metrics.
- Do not invent numbers.
- Do not recalculate risk.
- Keep the response concise.
- Provide 3 short bullet points.
- Focus on portfolio risk and collections prioritization.
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt,
    )

    return response.output_text


if __name__ == "__main__":
    summary = generate_portfolio_summary(
        total_accounts=500,
        total_exposure=10415348.65,
        total_expected_loss=3032184.00,
        highest_risk_grade="C",
        top_state="CA",
    )

    print(summary)