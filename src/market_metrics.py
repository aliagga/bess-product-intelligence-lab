from pathlib import Path

import pandas as pd


# ============================================================
# BESS Product Intelligence Lab
# Step 4A - Market Metrics
# ============================================================
#
# This module converts synthetic market data into product-facing
# market intelligence metrics.
#
# Output:
# - outputs/market_metrics.csv
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

MARKET_DATA_PATH = DATA_DIR / "sample_market_prices.csv"
MARKET_METRICS_OUTPUT_PATH = OUTPUT_DIR / "market_metrics.csv"


def load_market_data() -> pd.DataFrame:
    """
    Load synthetic market data.
    """

    if not MARKET_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Market data not found: {MARKET_DATA_PATH}. "
            "Run python generate_sample_data.py first."
        )

    market_df = pd.read_csv(MARKET_DATA_PATH)
    market_df["timestamp"] = pd.to_datetime(market_df["timestamp"])

    required_columns = {
        "timestamp",
        "day_ahead_price_eur_mwh",
        "fcr_price_eur_mw_h",
        "afrr_up_price_eur_mw_h",
        "afrr_down_price_eur_mw_h",
        "grid_constraint_score",
        "imbalance_risk_score",
    }

    missing_columns = required_columns - set(market_df.columns)

    if missing_columns:
        raise ValueError(f"Missing market columns: {missing_columns}")

    if market_df.empty:
        raise ValueError("Market dataframe is empty.")

    return market_df


def build_metric_record(
    metric_name: str,
    metric_value: float,
    unit: str,
    product_interpretation: str,
) -> dict:
    """
    Build one market metric record.
    """

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "unit": unit,
        "product_interpretation": product_interpretation,
    }


def calculate_market_metrics(market_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate product-facing market metrics.
    """

    market_df = market_df.copy()
    market_df["date"] = market_df["timestamp"].dt.date

    daily_spread = (
        market_df.groupby("date")["day_ahead_price_eur_mwh"]
        .agg(lambda series: series.max() - series.min())
        .mean()
    )

    high_price_threshold = market_df["day_ahead_price_eur_mwh"].quantile(0.80)
    low_price_threshold = market_df["day_ahead_price_eur_mwh"].quantile(0.20)

    high_price_hours = int(
        (market_df["day_ahead_price_eur_mwh"] >= high_price_threshold).sum()
    )

    low_price_hours = int(
        (market_df["day_ahead_price_eur_mwh"] <= low_price_threshold).sum()
    )

    negative_price_hours = int((market_df["day_ahead_price_eur_mwh"] < 0).sum())

    high_constraint_hours = int((market_df["grid_constraint_score"] >= 0.70).sum())
    medium_constraint_hours = int(
        (
            (market_df["grid_constraint_score"] >= 0.40)
            & (market_df["grid_constraint_score"] < 0.70)
        ).sum()
    )

    high_imbalance_risk_hours = int((market_df["imbalance_risk_score"] >= 0.70).sum())

    records = [
        build_metric_record(
            metric_name="Market time horizon",
            metric_value=len(market_df),
            unit="hours",
            product_interpretation=(
                "Shows the size of the market sample used in the V1 prototype."
            ),
        ),
        build_metric_record(
            metric_name="Average Day-Ahead price",
            metric_value=round(market_df["day_ahead_price_eur_mwh"].mean(), 2),
            unit="EUR/MWh",
            product_interpretation=(
                "Provides a baseline view of the energy-market price environment."
            ),
        ),
        build_metric_record(
            metric_name="Maximum Day-Ahead price",
            metric_value=round(market_df["day_ahead_price_eur_mwh"].max(), 2),
            unit="EUR/MWh",
            product_interpretation=(
                "Highlights high-price periods where discharge value may be strong."
            ),
        ),
        build_metric_record(
            metric_name="Minimum Day-Ahead price",
            metric_value=round(market_df["day_ahead_price_eur_mwh"].min(), 2),
            unit="EUR/MWh",
            product_interpretation=(
                "Highlights low-price or negative-price periods where charging may be attractive."
            ),
        ),
        build_metric_record(
            metric_name="Average daily Day-Ahead spread",
            metric_value=round(daily_spread, 2),
            unit="EUR/MWh",
            product_interpretation=(
                "Indicates arbitrage potential and the need for strategy comparison."
            ),
        ),
        build_metric_record(
            metric_name="High-price hours",
            metric_value=high_price_hours,
            unit="hours",
            product_interpretation=(
                "Represents hours where discharge or reserve activation value may be relevant."
            ),
        ),
        build_metric_record(
            metric_name="Low-price hours",
            metric_value=low_price_hours,
            unit="hours",
            product_interpretation=(
                "Represents hours where charging opportunities may exist."
            ),
        ),
        build_metric_record(
            metric_name="Negative-price hours",
            metric_value=negative_price_hours,
            unit="hours",
            product_interpretation=(
                "Supports product features around renewable surplus, charging recommendations, and price-event explanations."
            ),
        ),
        build_metric_record(
            metric_name="Average FCR price",
            metric_value=round(market_df["fcr_price_eur_mw_h"].mean(), 2),
            unit="EUR/MW/h",
            product_interpretation=(
                "Supports reserve-market revenue attribution and strategy comparison."
            ),
        ),
        build_metric_record(
            metric_name="Average aFRR up price",
            metric_value=round(market_df["afrr_up_price_eur_mw_h"].mean(), 2),
            unit="EUR/MW/h",
            product_interpretation=(
                "Shows the value potential of upward reserve participation."
            ),
        ),
        build_metric_record(
            metric_name="Average aFRR down price",
            metric_value=round(market_df["afrr_down_price_eur_mw_h"].mean(), 2),
            unit="EUR/MW/h",
            product_interpretation=(
                "Shows the value potential of downward reserve participation."
            ),
        ),
        build_metric_record(
            metric_name="High grid-constraint hours",
            metric_value=high_constraint_hours,
            unit="hours",
            product_interpretation=(
                "Supports the need for grid-constraint explainability and missed-revenue analysis."
            ),
        ),
        build_metric_record(
            metric_name="Medium grid-constraint hours",
            metric_value=medium_constraint_hours,
            unit="hours",
            product_interpretation=(
                "Indicates periods where asset operation may be partially limited."
            ),
        ),
        build_metric_record(
            metric_name="High imbalance-risk hours",
            metric_value=high_imbalance_risk_hours,
            unit="hours",
            product_interpretation=(
                "Supports future V2 features around risk-aware dispatch and forecast uncertainty."
            ),
        ),
    ]

    return pd.DataFrame(records)


def save_market_metrics() -> pd.DataFrame:
    """
    Calculate and save market metrics.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    market_df = load_market_data()
    metrics_df = calculate_market_metrics(market_df)

    metrics_df.to_csv(MARKET_METRICS_OUTPUT_PATH, index=False)

    return metrics_df


def print_summary(metrics_df: pd.DataFrame) -> None:
    """
    Print a simple terminal summary.
    """

    print("Market metrics generated successfully.")
    print(f"Output saved to: {MARKET_METRICS_OUTPUT_PATH}")
    print()
    print(metrics_df.to_string(index=False))


if __name__ == "__main__":
    output_df = save_market_metrics()
    print_summary(output_df)