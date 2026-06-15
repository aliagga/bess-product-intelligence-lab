from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# BESS Product Intelligence Lab
# Step 2 - Synthetic Sample Data Generator
# ============================================================
#
# This script creates three datasets:
# 1. sample_market_prices.csv
# 2. sample_bess_assets.csv
# 3. sample_product_usage.csv
#
# The data is synthetic and designed for product demonstration.
# It is not intended to represent actual trading results.
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"

RANDOM_SEED = 42


def create_market_price_data() -> pd.DataFrame:
    """
    Create synthetic hourly market data for BESS revenue scenarios.

    The generated data includes:
    - Day-ahead prices
    - FCR capacity prices
    - aFRR up capacity prices
    - aFRR down capacity prices
    - Grid constraint score
    - Imbalance risk score

    The values are synthetic but shaped to resemble realistic product-demo data.
    """

    rng = np.random.default_rng(RANDOM_SEED)

    start = "2026-01-01 00:00:00"
    periods = 14 * 24  # 14 days, hourly resolution

    timestamps = pd.date_range(start=start, periods=periods, freq="h")

    hours = timestamps.hour.to_numpy()
    weekdays = timestamps.dayofweek.to_numpy()

    # --------------------------------------------------------
    # Day-ahead price pattern
    # --------------------------------------------------------
    # Morning and evening peaks, lower prices overnight.
    # This creates arbitrage opportunities for the BESS.
    morning_peak = 45 * np.exp(-((hours - 8) ** 2) / 10)
    evening_peak = 65 * np.exp(-((hours - 19) ** 2) / 8)
    night_discount = -18 * np.exp(-((hours - 3) ** 2) / 8)

    weekday_effect = np.where(weekdays < 5, 8, -4)
    random_noise = rng.normal(0, 8, periods)

    day_ahead_price = (
        55
        + morning_peak
        + evening_peak
        + night_discount
        + weekday_effect
        + random_noise
    )

    # Add a few low/negative-price hours to mimic renewable-heavy periods.
    low_price_hours = rng.choice(periods, size=12, replace=False)
    day_ahead_price[low_price_hours] -= rng.uniform(45, 75, size=len(low_price_hours))

    day_ahead_price = np.round(np.asarray(day_ahead_price, dtype=float), 2)

    # --------------------------------------------------------
    # Reserve market price patterns
    # --------------------------------------------------------
    # FCR is smoother and more capacity-market-like.
    fcr_price = 18 + 5 * np.sin(2 * np.pi * hours / 24) + rng.normal(0, 2.5, periods)
    fcr_price = np.maximum(fcr_price, 2)
    fcr_price = np.round(fcr_price, 2)

    # aFRR up tends to be more valuable during high-demand periods.
    afrr_up_price = (
        8
        + 0.10 * np.maximum(day_ahead_price - 60, 0)
        + 4 * np.exp(-((hours - 19) ** 2) / 8)
        + rng.normal(0, 2.0, periods)
    )
    afrr_up_price = np.maximum(afrr_up_price, 0)
    afrr_up_price = np.round(afrr_up_price, 2)

    # aFRR down can become more valuable during low-price / surplus periods.
    afrr_down_price = (
        6
        + 0.08 * np.maximum(45 - day_ahead_price, 0)
        + 3 * np.exp(-((hours - 3) ** 2) / 8)
        + rng.normal(0, 1.8, periods)
    )
    afrr_down_price = np.maximum(afrr_down_price, 0)
    afrr_down_price = np.round(afrr_down_price, 2)

    # --------------------------------------------------------
    # Grid constraint and imbalance risk scores
    # --------------------------------------------------------
    # Scores between 0 and 1.
    # Higher grid constraint scores reduce usable grid connection in V1.
    evening_constraint = 0.55 * np.exp(-((hours - 19) ** 2) / 10)
    morning_constraint = 0.35 * np.exp(-((hours - 8) ** 2) / 12)
    random_constraint = rng.uniform(0, 0.20, periods)

    grid_constraint_score = evening_constraint + morning_constraint + random_constraint

    # Add a few strong constraint events.
    constraint_event_hours = rng.choice(periods, size=18, replace=False)
    grid_constraint_score[constraint_event_hours] += rng.uniform(
        0.30, 0.55, size=len(constraint_event_hours)
    )

    grid_constraint_score = np.clip(grid_constraint_score, 0, 1)
    grid_constraint_score = np.round(grid_constraint_score, 3)

    # Imbalance risk increases with price volatility and around peak hours.
    price_change = np.abs(np.diff(day_ahead_price, prepend=day_ahead_price[0]))
    normalized_price_change = price_change / max(price_change.max(), 1)

    imbalance_risk_score = (
        0.25 * normalized_price_change
        + 0.35 * np.exp(-((hours - 18) ** 2) / 10)
        + rng.uniform(0, 0.25, periods)
    )

    imbalance_risk_score = np.clip(imbalance_risk_score, 0, 1)
    imbalance_risk_score = np.round(imbalance_risk_score, 3)

    market_df = pd.DataFrame(
        {
            "timestamp": timestamps,
            "day_ahead_price_eur_mwh": day_ahead_price,
            "fcr_price_eur_mw_h": fcr_price,
            "afrr_up_price_eur_mw_h": afrr_up_price,
            "afrr_down_price_eur_mw_h": afrr_down_price,
            "grid_constraint_score": grid_constraint_score,
            "imbalance_risk_score": imbalance_risk_score,
        }
    )

    return market_df


def create_bess_asset_data() -> pd.DataFrame:
    """
    Create sample BESS asset data.

    The assets are intentionally different to support product comparisons:
    - Different countries
    - Different power and energy ratings
    - Different grid connection limits
    - Different commercial models
    """

    asset_data = [
        {
            "asset_id": "BESS_DE_01",
            "asset_name": "Germany Utility Scale Asset",
            "country": "Germany",
            "power_mw": 50.0,
            "energy_mwh": 100.0,
            "round_trip_efficiency": 0.88,
            "min_soc_mwh": 10.0,
            "max_soc_mwh": 95.0,
            "initial_soc_mwh": 50.0,
            "grid_connection_mw": 45.0,
            "commercial_model": "merchant",
            "asset_owner_type": "IPP",
        },
        {
            "asset_id": "BESS_DE_02",
            "asset_name": "Germany Investor-Backed Asset",
            "country": "Germany",
            "power_mw": 20.0,
            "energy_mwh": 55.0,
            "round_trip_efficiency": 0.90,
            "min_soc_mwh": 5.0,
            "max_soc_mwh": 52.0,
            "initial_soc_mwh": 25.0,
            "grid_connection_mw": 18.0,
            "commercial_model": "floor_style_revenue_protection",
            "asset_owner_type": "Infrastructure Investor",
        },
        {
            "asset_id": "BESS_ES_01",
            "asset_name": "Spain Co-location Candidate",
            "country": "Spain",
            "power_mw": 30.0,
            "energy_mwh": 60.0,
            "round_trip_efficiency": 0.89,
            "min_soc_mwh": 6.0,
            "max_soc_mwh": 57.0,
            "initial_soc_mwh": 30.0,
            "grid_connection_mw": 25.0,
            "commercial_model": "merchant",
            "asset_owner_type": "Renewable Developer",
        },
        {
            "asset_id": "BESS_PL_01",
            "asset_name": "Poland Market Entry Asset",
            "country": "Poland",
            "power_mw": 15.0,
            "energy_mwh": 30.0,
            "round_trip_efficiency": 0.87,
            "min_soc_mwh": 3.0,
            "max_soc_mwh": 28.0,
            "initial_soc_mwh": 15.0,
            "grid_connection_mw": 12.0,
            "commercial_model": "market_entry_pilot",
            "asset_owner_type": "Municipal Utility",
        },
    ]

    return pd.DataFrame(asset_data)


def create_product_usage_data(asset_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create sample product usage and customer-health data.

    This supports the product-management side of the dashboard.
    """

    rng = np.random.default_rng(RANDOM_SEED + 1)

    customer_map = {
        "BESS_DE_01": "CUST_IPP_001",
        "BESS_DE_02": "CUST_INV_002",
        "BESS_ES_01": "CUST_DEV_003",
        "BESS_PL_01": "CUST_MUNI_004",
    }

    rows = []

    months = ["2026-01", "2026-02", "2026-03"]

    for _, asset in asset_df.iterrows():
        asset_id = asset["asset_id"]
        customer_id = customer_map[asset_id]

        for month in months:
            dashboard_views = int(rng.integers(8, 45))
            report_downloads = int(rng.integers(2, 18))
            support_tickets = int(rng.integers(0, 8))
            manual_overrides = int(rng.integers(0, 12))

            optimizer_success_rate = np.round(rng.uniform(0.91, 0.995), 3)

            # Simple customer health proxy.
            # Higher engagement and reliability increase score.
            # More support tickets and overrides reduce score.
            customer_health_score = (
                55
                + 0.7 * dashboard_views
                + 1.2 * report_downloads
                + 30 * (optimizer_success_rate - 0.90)
                - 3.5 * support_tickets
                - 1.5 * manual_overrides
            )

            customer_health_score = float(np.clip(customer_health_score, 0, 100))
            customer_health_score = round(customer_health_score, 1)

            rows.append(
                {
                    "customer_id": customer_id,
                    "asset_id": asset_id,
                    "month": month,
                    "dashboard_views": dashboard_views,
                    "report_downloads": report_downloads,
                    "support_tickets": support_tickets,
                    "manual_overrides": manual_overrides,
                    "optimizer_success_rate": optimizer_success_rate,
                    "customer_health_score": customer_health_score,
                }
            )

    return pd.DataFrame(rows)


def validate_data(
    market_df: pd.DataFrame,
    asset_df: pd.DataFrame,
    usage_df: pd.DataFrame,
) -> None:
    """
    Run basic validation checks before saving.
    """

    required_market_columns = {
        "timestamp",
        "day_ahead_price_eur_mwh",
        "fcr_price_eur_mw_h",
        "afrr_up_price_eur_mw_h",
        "afrr_down_price_eur_mw_h",
        "grid_constraint_score",
        "imbalance_risk_score",
    }

    required_asset_columns = {
        "asset_id",
        "asset_name",
        "country",
        "power_mw",
        "energy_mwh",
        "round_trip_efficiency",
        "min_soc_mwh",
        "max_soc_mwh",
        "initial_soc_mwh",
        "grid_connection_mw",
        "commercial_model",
        "asset_owner_type",
    }

    required_usage_columns = {
        "customer_id",
        "asset_id",
        "month",
        "dashboard_views",
        "report_downloads",
        "support_tickets",
        "manual_overrides",
        "optimizer_success_rate",
        "customer_health_score",
    }

    missing_market_cols = required_market_columns - set(market_df.columns)
    missing_asset_cols = required_asset_columns - set(asset_df.columns)
    missing_usage_cols = required_usage_columns - set(usage_df.columns)

    if missing_market_cols:
        raise ValueError(f"Missing market columns: {missing_market_cols}")

    if missing_asset_cols:
        raise ValueError(f"Missing asset columns: {missing_asset_cols}")

    if missing_usage_cols:
        raise ValueError(f"Missing product usage columns: {missing_usage_cols}")

    if market_df.empty:
        raise ValueError("Market dataframe is empty.")

    if asset_df.empty:
        raise ValueError("Asset dataframe is empty.")

    if usage_df.empty:
        raise ValueError("Product usage dataframe is empty.")

    if not usage_df["asset_id"].isin(asset_df["asset_id"]).all():
        raise ValueError("Some usage asset IDs do not exist in asset data.")

    if not market_df["grid_constraint_score"].between(0, 1).all():
        raise ValueError("Grid constraint score must be between 0 and 1.")

    if not market_df["imbalance_risk_score"].between(0, 1).all():
        raise ValueError("Imbalance risk score must be between 0 and 1.")

    if not usage_df["customer_health_score"].between(0, 100).all():
        raise ValueError("Customer health score must be between 0 and 100.")


def save_datasets() -> None:
    """
    Generate, validate, and save all sample datasets.
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    market_df = create_market_price_data()
    asset_df = create_bess_asset_data()
    usage_df = create_product_usage_data(asset_df)

    validate_data(market_df, asset_df, usage_df)

    market_path = DATA_DIR / "sample_market_prices.csv"
    asset_path = DATA_DIR / "sample_bess_assets.csv"
    usage_path = DATA_DIR / "sample_product_usage.csv"

    market_df.to_csv(market_path, index=False)
    asset_df.to_csv(asset_path, index=False)
    usage_df.to_csv(usage_path, index=False)

    print("Sample datasets generated successfully.")
    print(f"Market data: {market_path}")
    print(f"BESS assets: {asset_path}")
    print(f"Product usage: {usage_path}")
    print()
    print("Summary:")
    print(f"- Market rows: {len(market_df)}")
    print(f"- Asset rows: {len(asset_df)}")
    print(f"- Product usage rows: {len(usage_df)}")
    print()
    print("Market price range:")
    print(
        f"- Day-ahead min/max: "
        f"{market_df['day_ahead_price_eur_mwh'].min():.2f} / "
        f"{market_df['day_ahead_price_eur_mwh'].max():.2f} EUR/MWh"
    )
    print(
        f"- FCR min/max: "
        f"{market_df['fcr_price_eur_mw_h'].min():.2f} / "
        f"{market_df['fcr_price_eur_mw_h'].max():.2f} EUR/MW/h"
    )


if __name__ == "__main__":
    save_datasets()