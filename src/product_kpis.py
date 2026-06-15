from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd


# ============================================================
# BESS Product Intelligence Lab
# Step 4B - Product KPIs and Roadmap Prioritization
# ============================================================
#
# This module converts scenario results and product usage data into:
# 1. Asset-level product/commercial KPIs
# 2. Roadmap prioritization using RICE-style scoring
#
# Outputs:
# - outputs/asset_kpis.csv
# - outputs/roadmap_prioritization.csv
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

ASSET_DATA_PATH = DATA_DIR / "sample_bess_assets.csv"
USAGE_DATA_PATH = DATA_DIR / "sample_product_usage.csv"
REVENUE_SCENARIOS_PATH = OUTPUT_DIR / "revenue_scenarios.csv"

ASSET_KPIS_OUTPUT_PATH = OUTPUT_DIR / "asset_kpis.csv"
ROADMAP_OUTPUT_PATH = OUTPUT_DIR / "roadmap_prioritization.csv"


# ------------------------------------------------------------
# Loading and validation
# ------------------------------------------------------------

def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load asset data, product usage data, and revenue scenario outputs.
    """

    if not ASSET_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Asset data not found: {ASSET_DATA_PATH}. "
            "Run python generate_sample_data.py first."
        )

    if not USAGE_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Product usage data not found: {USAGE_DATA_PATH}. "
            "Run python generate_sample_data.py first."
        )

    if not REVENUE_SCENARIOS_PATH.exists():
        raise FileNotFoundError(
            f"Revenue scenario output not found: {REVENUE_SCENARIOS_PATH}. "
            "Run python src/bess_simulator.py first."
        )

    asset_df = pd.read_csv(ASSET_DATA_PATH)
    usage_df = pd.read_csv(USAGE_DATA_PATH)
    revenue_df = pd.read_csv(REVENUE_SCENARIOS_PATH)

    validate_inputs(asset_df, usage_df, revenue_df)

    return asset_df, usage_df, revenue_df


def validate_inputs(
    asset_df: pd.DataFrame,
    usage_df: pd.DataFrame,
    revenue_df: pd.DataFrame,
) -> None:
    """
    Validate required input columns.
    """

    required_asset_columns = {
        "asset_id",
        "asset_name",
        "country",
        "power_mw",
        "energy_mwh",
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

    required_revenue_columns = {
        "asset_id",
        "asset_name",
        "country",
        "asset_owner_type",
        "commercial_model",
        "scenario",
        "day_ahead_revenue_eur",
        "fcr_revenue_eur",
        "afrr_revenue_eur",
        "total_revenue_eur",
        "revenue_per_mw_eur",
        "revenue_per_mwh_eur",
        "constraint_binding_hours",
        "missed_revenue_eur",
        "dominant_market",
        "product_recommendation",
    }

    missing_asset_cols = required_asset_columns - set(asset_df.columns)
    missing_usage_cols = required_usage_columns - set(usage_df.columns)
    missing_revenue_cols = required_revenue_columns - set(revenue_df.columns)

    if missing_asset_cols:
        raise ValueError(f"Missing asset columns: {missing_asset_cols}")

    if missing_usage_cols:
        raise ValueError(f"Missing usage columns: {missing_usage_cols}")

    if missing_revenue_cols:
        raise ValueError(f"Missing revenue columns: {missing_revenue_cols}")

    if asset_df.empty:
        raise ValueError("Asset dataframe is empty.")

    if usage_df.empty:
        raise ValueError("Usage dataframe is empty.")

    if revenue_df.empty:
        raise ValueError("Revenue scenario dataframe is empty.")


# ------------------------------------------------------------
# Asset KPI logic
# ------------------------------------------------------------

def get_best_scenario_per_asset(revenue_df: pd.DataFrame) -> pd.DataFrame:
    """
    Select the highest-revenue scenario for each asset.
    """

    idx = revenue_df.groupby("asset_id")["total_revenue_eur"].idxmax()
    best_df = revenue_df.loc[idx].copy()

    best_df = best_df.rename(
        columns={
            "scenario": "best_scenario",
            "total_revenue_eur": "best_scenario_revenue_eur",
            "revenue_per_mw_eur": "best_revenue_per_mw_eur",
            "revenue_per_mwh_eur": "best_revenue_per_mwh_eur",
            "dominant_market": "best_dominant_market",
            "product_recommendation": "best_product_recommendation",
        }
    )

    selected_columns = [
        "asset_id",
        "best_scenario",
        "best_scenario_revenue_eur",
        "best_revenue_per_mw_eur",
        "best_revenue_per_mwh_eur",
        "best_dominant_market",
        "best_product_recommendation",
    ]

    return best_df[selected_columns]


def get_day_ahead_baseline(revenue_df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract Day-Ahead-only revenue as a baseline.
    """

    baseline_df = revenue_df[revenue_df["scenario"] == "Day-Ahead Only"].copy()

    baseline_df = baseline_df.rename(
        columns={
            "total_revenue_eur": "day_ahead_baseline_revenue_eur",
            "revenue_per_mw_eur": "day_ahead_baseline_revenue_per_mw_eur",
        }
    )

    return baseline_df[
        [
            "asset_id",
            "day_ahead_baseline_revenue_eur",
            "day_ahead_baseline_revenue_per_mw_eur",
        ]
    ]


def get_grid_constraint_metrics(revenue_df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract metrics from the grid-constrained scenario.
    """

    grid_df = revenue_df[
        revenue_df["scenario"] == "Grid-Constrained Hybrid"
    ].copy()

    grid_df = grid_df.rename(
        columns={
            "constraint_binding_hours": "grid_constraint_binding_hours",
            "missed_revenue_eur": "grid_missed_revenue_eur",
            "product_recommendation": "grid_constraint_product_recommendation",
        }
    )

    return grid_df[
        [
            "asset_id",
            "grid_constraint_binding_hours",
            "grid_missed_revenue_eur",
            "grid_constraint_product_recommendation",
        ]
    ]


def aggregate_product_usage(usage_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate product usage data at asset level.
    """

    usage_agg = (
        usage_df.groupby("asset_id")
        .agg(
            customer_id=("customer_id", "first"),
            total_dashboard_views=("dashboard_views", "sum"),
            total_report_downloads=("report_downloads", "sum"),
            total_support_tickets=("support_tickets", "sum"),
            total_manual_overrides=("manual_overrides", "sum"),
            average_optimizer_success_rate=("optimizer_success_rate", "mean"),
            average_customer_health_score=("customer_health_score", "mean"),
        )
        .reset_index()
    )

    usage_agg["average_optimizer_success_rate"] = usage_agg[
        "average_optimizer_success_rate"
    ].round(3)

    usage_agg["average_customer_health_score"] = usage_agg[
        "average_customer_health_score"
    ].round(1)

    return usage_agg


def calculate_revenue_uplift(asset_kpi_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate uplift of best scenario vs Day-Ahead-only baseline.
    """

    df = asset_kpi_df.copy()

    df["revenue_uplift_vs_day_ahead_eur"] = (
        df["best_scenario_revenue_eur"]
        - df["day_ahead_baseline_revenue_eur"]
    ).round(2)

    df["revenue_uplift_vs_day_ahead_pct"] = np.where(
        df["day_ahead_baseline_revenue_eur"].abs() > 1e-6,
        100
        * df["revenue_uplift_vs_day_ahead_eur"]
        / df["day_ahead_baseline_revenue_eur"].abs(),
        0,
    )

    df["revenue_uplift_vs_day_ahead_pct"] = df[
        "revenue_uplift_vs_day_ahead_pct"
    ].round(2)

    return df


def calculate_product_opportunity_score(asset_kpi_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate a simple 0-100 product opportunity score.

    Higher scores indicate assets/customers where product improvements
    may create stronger value or reduce friction.
    """

    df = asset_kpi_df.copy()

    max_revenue = max(df["best_scenario_revenue_eur"].max(), 1)
    max_missed_revenue = max(df["grid_missed_revenue_eur"].max(), 1)
    max_support_tickets = max(df["total_support_tickets"].max(), 1)
    max_manual_overrides = max(df["total_manual_overrides"].max(), 1)

    revenue_component = 30 * df["best_scenario_revenue_eur"] / max_revenue
    missed_revenue_component = 25 * df["grid_missed_revenue_eur"] / max_missed_revenue
    support_component = 15 * df["total_support_tickets"] / max_support_tickets
    override_component = 10 * df["total_manual_overrides"] / max_manual_overrides

    health_gap_component = 20 * (
        1 - df["average_customer_health_score"].clip(0, 100) / 100
    )

    df["product_opportunity_score"] = (
        revenue_component
        + missed_revenue_component
        + support_component
        + override_component
        + health_gap_component
    ).round(1)

    df["product_opportunity_level"] = pd.cut(
        df["product_opportunity_score"],
        bins=[-1, 35, 65, 100],
        labels=["Low", "Medium", "High"],
    ).astype(str)

    return df


def assign_primary_product_need(row: pd.Series) -> str:
    """
    Assign a primary product need based on KPI signals.
    """

    if row["grid_missed_revenue_eur"] > 0.10 * max(row["best_scenario_revenue_eur"], 1):
        return "Grid Constraint Explainability"

    if row["total_support_tickets"] >= 10:
        return "Automated Customer Reporting"

    if row["total_manual_overrides"] >= 15:
        return "Operational Alert Intelligence"

    if row["best_dominant_market"] in {"fcr", "afrr"}:
        return "Reserve Market Revenue Attribution"

    if row["revenue_uplift_vs_day_ahead_pct"] > 30:
        return "Market Strategy Scenario Explorer"

    return "Monthly Revenue Explanation Report"


def build_asset_kpis(
    asset_df: pd.DataFrame,
    usage_df: pd.DataFrame,
    revenue_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build asset-level product and commercial KPIs.
    """

    best_scenario_df = get_best_scenario_per_asset(revenue_df)
    baseline_df = get_day_ahead_baseline(revenue_df)
    grid_constraint_df = get_grid_constraint_metrics(revenue_df)
    usage_agg_df = aggregate_product_usage(usage_df)

    asset_kpi_df = asset_df.merge(best_scenario_df, on="asset_id", how="left")
    asset_kpi_df = asset_kpi_df.merge(baseline_df, on="asset_id", how="left")
    asset_kpi_df = asset_kpi_df.merge(grid_constraint_df, on="asset_id", how="left")
    asset_kpi_df = asset_kpi_df.merge(usage_agg_df, on="asset_id", how="left")

    asset_kpi_df = calculate_revenue_uplift(asset_kpi_df)
    asset_kpi_df = calculate_product_opportunity_score(asset_kpi_df)

    asset_kpi_df["primary_product_need"] = asset_kpi_df.apply(
        assign_primary_product_need,
        axis=1,
    )

    selected_columns = [
        "asset_id",
        "asset_name",
        "country",
        "asset_owner_type",
        "commercial_model",
        "power_mw",
        "energy_mwh",
        "customer_id",
        "best_scenario",
        "best_scenario_revenue_eur",
        "best_revenue_per_mw_eur",
        "best_revenue_per_mwh_eur",
        "day_ahead_baseline_revenue_eur",
        "revenue_uplift_vs_day_ahead_eur",
        "revenue_uplift_vs_day_ahead_pct",
        "best_dominant_market",
        "grid_constraint_binding_hours",
        "grid_missed_revenue_eur",
        "total_dashboard_views",
        "total_report_downloads",
        "total_support_tickets",
        "total_manual_overrides",
        "average_optimizer_success_rate",
        "average_customer_health_score",
        "product_opportunity_score",
        "product_opportunity_level",
        "primary_product_need",
        "best_product_recommendation",
    ]

    return asset_kpi_df[selected_columns]


# ------------------------------------------------------------
# Roadmap prioritization logic
# ------------------------------------------------------------

def build_roadmap_features(asset_kpi_df: pd.DataFrame) -> List[Dict[str, object]]:
    """
    Build roadmap feature candidates.

    Scoring uses a RICE-style method:
    RICE = Reach * Impact * Confidence / Effort
    """

    total_assets = len(asset_kpi_df)

    assets_with_constraints = int((asset_kpi_df["grid_missed_revenue_eur"] > 0).sum())
    assets_with_support_burden = int((asset_kpi_df["total_support_tickets"] >= 8).sum())
    assets_with_manual_overrides = int((asset_kpi_df["total_manual_overrides"] >= 10).sum())
    assets_with_high_uplift = int(
        (asset_kpi_df["revenue_uplift_vs_day_ahead_pct"] > 30).sum()
    )

    reserve_market_assets = int(
        asset_kpi_df["best_dominant_market"].isin(["fcr", "afrr"]).sum()
    )

    investor_assets = int(
        asset_kpi_df["asset_owner_type"]
        .str.contains("Investor", case=False, na=False)
        .sum()
    )

    colocation_assets = int(
        asset_kpi_df["asset_name"]
        .str.contains("Co-location", case=False, na=False)
        .sum()
    )

    features = [
        {
            "feature": "Revenue Attribution Engine",
            "target_user": "Asset owner, investor, sales, customer success",
            "problem": "Customers need to understand where battery revenue comes from across DA, FCR, and aFRR.",
            "evidence_signal": f"{reserve_market_assets} assets have reserve-market-dominant or reserve-relevant revenue.",
            "reach": max(total_assets, 1),
            "impact": 9,
            "confidence": 0.85,
            "effort": 4,
        },
        {
            "feature": "Grid Constraint Explainability",
            "target_user": "Asset owner, operations, trader, product team",
            "problem": "Grid constraints can reduce dispatch capacity and create missed revenue that needs to be explained.",
            "evidence_signal": f"{assets_with_constraints} assets show missed revenue in the constrained scenario.",
            "reach": max(assets_with_constraints, 1),
            "impact": 9,
            "confidence": 0.80,
            "effort": 5,
        },
        {
            "feature": "Market Strategy Scenario Explorer",
            "target_user": "Asset owner, product team, sales, investor",
            "problem": "Customers need to compare DA-only, reserve-only, and hybrid strategies before trusting the product.",
            "evidence_signal": f"{assets_with_high_uplift} assets show strong uplift versus DA-only baseline.",
            "reach": max(total_assets, 1),
            "impact": 8,
            "confidence": 0.85,
            "effort": 5,
        },
        {
            "feature": "Customer Monthly Report Generator",
            "target_user": "Customer success, sales, asset owner",
            "problem": "Customers need recurring explanations of revenue, missed value, constraints, and product performance.",
            "evidence_signal": f"{assets_with_support_burden} assets show higher support-ticket burden.",
            "reach": max(total_assets, 1),
            "impact": 8,
            "confidence": 0.75,
            "effort": 4,
        },
        {
            "feature": "Operational Alert Intelligence",
            "target_user": "Operations, trading, customer success",
            "problem": "Manual overrides and operational friction should trigger product alerts and workflow improvements.",
            "evidence_signal": f"{assets_with_manual_overrides} assets show elevated manual override activity.",
            "reach": max(assets_with_manual_overrides, 1),
            "impact": 7,
            "confidence": 0.70,
            "effort": 5,
        },
        {
            "feature": "Investor Risk Dashboard",
            "target_user": "Infrastructure investor, asset owner, commercial team",
            "problem": "Investors need revenue stability, scenario comparison, and risk explanation before committing capital.",
            "evidence_signal": f"{investor_assets} assets are investor-backed in the sample portfolio.",
            "reach": max(investor_assets, 1),
            "impact": 8,
            "confidence": 0.70,
            "effort": 6,
        },
        {
            "feature": "Co-location View",
            "target_user": "Renewable developer, IPP, product team",
            "problem": "PV+BESS co-location requires visibility into shared grid connection limits and curtailment reduction.",
            "evidence_signal": f"{colocation_assets} assets are marked as co-location candidates.",
            "reach": max(colocation_assets, 1),
            "impact": 7,
            "confidence": 0.65,
            "effort": 7,
        },
        {
            "feature": "Floor-Style Revenue Comparison",
            "target_user": "Investor, asset owner, commercial team",
            "problem": "Customers comparing merchant and protected-revenue models need transparent upside/downside analysis.",
            "evidence_signal": "One sample asset uses a floor-style revenue protection concept.",
            "reach": 1,
            "impact": 8,
            "confidence": 0.65,
            "effort": 6,
        },
        {
            "feature": "Product Health Scoring",
            "target_user": "Product manager, customer success, leadership",
            "problem": "The product team needs a repeatable way to identify customers/assets needing attention.",
            "evidence_signal": "All sample assets have product-usage and customer-health data.",
            "reach": max(total_assets, 1),
            "impact": 7,
            "confidence": 0.80,
            "effort": 3,
        },
    ]

    return features


def calculate_roadmap_prioritization(asset_kpi_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate RICE-style roadmap prioritization.
    """

    features = build_roadmap_features(asset_kpi_df)
    roadmap_df = pd.DataFrame(features)

    roadmap_df["rice_score"] = (
        roadmap_df["reach"]
        * roadmap_df["impact"]
        * roadmap_df["confidence"]
        / roadmap_df["effort"]
    ).round(2)

    roadmap_df = roadmap_df.sort_values(
        by="rice_score",
        ascending=False,
    ).reset_index(drop=True)

    roadmap_df["priority_rank"] = roadmap_df.index + 1

    roadmap_df["priority_level"] = pd.cut(
        roadmap_df["rice_score"],
        bins=[-1, 3, 6, 100],
        labels=["Low", "Medium", "High"],
    ).astype(str)

    selected_columns = [
        "priority_rank",
        "feature",
        "priority_level",
        "rice_score",
        "reach",
        "impact",
        "confidence",
        "effort",
        "target_user",
        "problem",
        "evidence_signal",
    ]

    return roadmap_df[selected_columns]


# ------------------------------------------------------------
# Main save function
# ------------------------------------------------------------

def save_product_kpis_and_roadmap() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generate and save asset KPIs and roadmap prioritization.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    asset_df, usage_df, revenue_df = load_inputs()

    asset_kpi_df = build_asset_kpis(
        asset_df=asset_df,
        usage_df=usage_df,
        revenue_df=revenue_df,
    )

    roadmap_df = calculate_roadmap_prioritization(asset_kpi_df)

    asset_kpi_df.to_csv(ASSET_KPIS_OUTPUT_PATH, index=False)
    roadmap_df.to_csv(ROADMAP_OUTPUT_PATH, index=False)

    return asset_kpi_df, roadmap_df


def print_summary(asset_kpi_df: pd.DataFrame, roadmap_df: pd.DataFrame) -> None:
    """
    Print a concise terminal summary.
    """

    print("Product KPIs and roadmap prioritization generated successfully.")
    print(f"Asset KPIs saved to: {ASSET_KPIS_OUTPUT_PATH}")
    print(f"Roadmap prioritization saved to: {ROADMAP_OUTPUT_PATH}")
    print()

    print("Asset KPI summary:")
    for _, row in asset_kpi_df.iterrows():
        print(
            f"- {row['asset_id']} | Best scenario: {row['best_scenario']} | "
            f"Revenue: {row['best_scenario_revenue_eur']:.2f} EUR | "
            f"Primary need: {row['primary_product_need']}"
        )

    print()
    print("Top roadmap priorities:")
    for _, row in roadmap_df.head(5).iterrows():
        print(
            f"- #{row['priority_rank']} {row['feature']} | "
            f"RICE: {row['rice_score']} | "
            f"Level: {row['priority_level']}"
        )


if __name__ == "__main__":
    asset_kpis, roadmap = save_product_kpis_and_roadmap()
    print_summary(asset_kpis, roadmap)