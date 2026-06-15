from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# BESS Product Intelligence Lab
# Step 5 - Streamlit Dashboard
# ============================================================
#
# This dashboard presents the V1 product sprint:
# - Market intelligence
# - Revenue scenario comparison
# - Asset/product KPIs
# - Grid constraint impact
# - Roadmap prioritization
# - V2 roadmap
#
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

MARKET_DATA_PATH = DATA_DIR / "sample_market_prices.csv"
ASSET_DATA_PATH = DATA_DIR / "sample_bess_assets.csv"
USAGE_DATA_PATH = DATA_DIR / "sample_product_usage.csv"

MARKET_METRICS_PATH = OUTPUT_DIR / "market_metrics.csv"
REVENUE_SCENARIOS_PATH = OUTPUT_DIR / "revenue_scenarios.csv"
ASSET_KPIS_PATH = OUTPUT_DIR / "asset_kpis.csv"
ROADMAP_PATH = OUTPUT_DIR / "roadmap_prioritization.csv"


# ------------------------------------------------------------
# Page setup
# ------------------------------------------------------------

st.set_page_config(
    page_title="BESS Product Intelligence Lab",
    page_icon="🔋",
    layout="wide",
)


# ------------------------------------------------------------
# Data loading
# ------------------------------------------------------------

@st.cache_data
def load_csv(path: Path) -> pd.DataFrame:
    """
    Load a CSV file with basic validation.
    """

    if not path.exists():
        st.error(
            f"Missing required file: {path}. "
            "Run the full workflow first:\n\n"
            "python generate_sample_data.py\n"
            "python src/bess_simulator.py\n"
            "python src/market_metrics.py\n"
            "python src/product_kpis.py"
        )
        st.stop()

    return pd.read_csv(path)


@st.cache_data
def load_all_data() -> dict:
    """
    Load all dashboard datasets.
    """

    market_df = load_csv(MARKET_DATA_PATH)
    asset_df = load_csv(ASSET_DATA_PATH)
    usage_df = load_csv(USAGE_DATA_PATH)
    market_metrics_df = load_csv(MARKET_METRICS_PATH)
    revenue_df = load_csv(REVENUE_SCENARIOS_PATH)
    asset_kpis_df = load_csv(ASSET_KPIS_PATH)
    roadmap_df = load_csv(ROADMAP_PATH)

    market_df["timestamp"] = pd.to_datetime(market_df["timestamp"])

    return {
        "market": market_df,
        "assets": asset_df,
        "usage": usage_df,
        "market_metrics": market_metrics_df,
        "revenue": revenue_df,
        "asset_kpis": asset_kpis_df,
        "roadmap": roadmap_df,
    }


data = load_all_data()

market_df = data["market"]
asset_df = data["assets"]
usage_df = data["usage"]
market_metrics_df = data["market_metrics"]
revenue_df = data["revenue"]
asset_kpis_df = data["asset_kpis"]
roadmap_df = data["roadmap"]


# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def format_eur(value: float) -> str:
    return f"€{value:,.0f}"


def format_pct(value: float) -> str:
    return f"{value:.1f}%"


def safe_get_metric(metric_name: str, default: float = 0.0) -> float:
    """
    Extract metric value from market metrics table.
    """

    match = market_metrics_df[market_metrics_df["metric_name"] == metric_name]

    if match.empty:
        return default

    return float(match["metric_value"].iloc[0])


def show_section_header(title: str, subtitle: str) -> None:
    """
    Standard section header.
    """

    st.markdown("---")
    st.header(title)
    st.caption(subtitle)


# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------

st.sidebar.title("🔋 BESS Product Intelligence Lab")
st.sidebar.markdown("**Product Sprint V1**")
st.sidebar.markdown(
    """
    This dashboard demonstrates how battery-storage revenue scenarios,
    product KPIs, market signals, and roadmap prioritization can support
    grid-scale BESS software decisions.
    """
)

available_assets = sorted(asset_df["asset_id"].unique().tolist())
selected_assets = st.sidebar.multiselect(
    "Select BESS assets",
    options=available_assets,
    default=available_assets,
)

available_scenarios = sorted(revenue_df["scenario"].unique().tolist())
selected_scenarios = st.sidebar.multiselect(
    "Select revenue scenarios",
    options=available_scenarios,
    default=available_scenarios,
)

filtered_revenue_df = revenue_df[
    revenue_df["asset_id"].isin(selected_assets)
    & revenue_df["scenario"].isin(selected_scenarios)
].copy()

filtered_asset_kpis_df = asset_kpis_df[
    asset_kpis_df["asset_id"].isin(selected_assets)
].copy()


# ------------------------------------------------------------
# Main title
# ------------------------------------------------------------

st.title("🔋 BESS Product Intelligence Lab")
st.subheader("Product Sprint V1: Battery Storage Market Intelligence + Product KPIs")

st.markdown(
    """
    This dashboard is a compact product portfolio prototype. It connects battery-storage
    revenue scenario logic with product-management decisions: customer value, market strategy,
    grid-constraint explainability, product KPIs, and roadmap prioritization.

    The objective is not to replicate a production trading platform. The objective is to show
    how a Senior Product Manager can translate energy-market complexity into product requirements,
    measurable KPIs, and roadmap decisions.
    """
)

st.info(
    "V1 uses synthetic sample data for demonstration. V2 is planned to add real market data, "
    "optimization-based dispatch, degradation logic, forecasting, co-location, and customer reporting."
)


# ------------------------------------------------------------
# 1. Executive Overview
# ------------------------------------------------------------

show_section_header(
    "1. Executive Overview",
    "High-level portfolio, revenue, constraint, and roadmap signals.",
)

total_assets = asset_df["asset_id"].nunique()
total_scenarios = revenue_df["scenario"].nunique()
best_total_revenue = filtered_asset_kpis_df["best_scenario_revenue_eur"].sum()
avg_customer_health = filtered_asset_kpis_df["average_customer_health_score"].mean()
total_missed_revenue = filtered_asset_kpis_df["grid_missed_revenue_eur"].sum()
top_roadmap_feature = roadmap_df.sort_values("priority_rank").iloc[0]["feature"]

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Sample Assets", total_assets)
col2.metric("Scenarios", total_scenarios)
col3.metric("Best Scenario Revenue", format_eur(best_total_revenue))
col4.metric("Avg Customer Health", f"{avg_customer_health:.1f}/100")
col5.metric("Missed Revenue", format_eur(total_missed_revenue))

st.markdown(
    f"""
    **Top roadmap priority:** `{top_roadmap_feature}`

    Product interpretation: the V1 prototype is designed to identify where the product should
    create clearer explanations, stronger customer reporting, and better market-strategy visibility.
    """
)


# ------------------------------------------------------------
# 2. Market Intelligence
# ------------------------------------------------------------

show_section_header(
    "2. Market Intelligence",
    "Market signals used by the V1 prototype to create revenue and product insights.",
)

avg_da_price = safe_get_metric("Average Day-Ahead price")
avg_daily_spread = safe_get_metric("Average daily Day-Ahead spread")
avg_fcr_price = safe_get_metric("Average FCR price")
high_constraint_hours = safe_get_metric("High grid-constraint hours")
high_imbalance_hours = safe_get_metric("High imbalance-risk hours")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Avg DA Price", f"{avg_da_price:.1f} €/MWh")
col2.metric("Avg Daily Spread", f"{avg_daily_spread:.1f} €/MWh")
col3.metric("Avg FCR Price", f"{avg_fcr_price:.1f} €/MW/h")
col4.metric("High Constraint Hours", f"{high_constraint_hours:.0f}")
col5.metric("High Imbalance Hours", f"{high_imbalance_hours:.0f}")

fig_da = px.line(
    market_df,
    x="timestamp",
    y="day_ahead_price_eur_mwh",
    title="Synthetic Day-Ahead Price Signal",
    labels={
        "timestamp": "Timestamp",
        "day_ahead_price_eur_mwh": "Day-Ahead Price (€/MWh)",
    },
)

st.plotly_chart(fig_da, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    fig_reserve = px.line(
        market_df,
        x="timestamp",
        y=[
            "fcr_price_eur_mw_h",
            "afrr_up_price_eur_mw_h",
            "afrr_down_price_eur_mw_h",
        ],
        title="Synthetic Reserve Market Price Signals",
        labels={
            "timestamp": "Timestamp",
            "value": "Price (€/MW/h)",
            "variable": "Market",
        },
    )
    st.plotly_chart(fig_reserve, use_container_width=True)

with col2:
    fig_constraints = px.line(
        market_df,
        x="timestamp",
        y=["grid_constraint_score", "imbalance_risk_score"],
        title="Grid Constraint and Imbalance Risk Signals",
        labels={
            "timestamp": "Timestamp",
            "value": "Score",
            "variable": "Signal",
        },
    )
    st.plotly_chart(fig_constraints, use_container_width=True)

with st.expander("View market metrics table"):
    st.dataframe(market_metrics_df, use_container_width=True)


# ------------------------------------------------------------
# 3. Revenue Scenario Comparison
# ------------------------------------------------------------

show_section_header(
    "3. Revenue Scenario Comparison",
    "Comparison of DA, FCR, aFRR, hybrid, and grid-constrained BESS strategies.",
)

if filtered_revenue_df.empty:
    st.warning("No revenue data available for the selected filters.")
else:
    fig_revenue = px.bar(
        filtered_revenue_df,
        x="scenario",
        y="total_revenue_eur",
        color="asset_id",
        barmode="group",
        title="Total Revenue by Scenario and Asset",
        labels={
            "scenario": "Scenario",
            "total_revenue_eur": "Total Revenue (€)",
            "asset_id": "Asset",
        },
    )

    st.plotly_chart(fig_revenue, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        market_share_df = filtered_revenue_df.melt(
            id_vars=["asset_id", "scenario"],
            value_vars=[
                "market_share_day_ahead_pct",
                "market_share_fcr_pct",
                "market_share_afrr_pct",
            ],
            var_name="market",
            value_name="share_pct",
        )

        market_share_df["market"] = market_share_df["market"].replace(
            {
                "market_share_day_ahead_pct": "Day-Ahead",
                "market_share_fcr_pct": "FCR",
                "market_share_afrr_pct": "aFRR",
            }
        )

        fig_market_share = px.bar(
            market_share_df,
            x="scenario",
            y="share_pct",
            color="market",
            title="Market Revenue Share by Scenario",
            labels={
                "scenario": "Scenario",
                "share_pct": "Revenue Share (%)",
                "market": "Market",
            },
        )

        st.plotly_chart(fig_market_share, use_container_width=True)

    with col2:
        fig_revenue_per_mw = px.bar(
            filtered_revenue_df,
            x="scenario",
            y="revenue_per_mw_eur",
            color="asset_id",
            barmode="group",
            title="Revenue per MW by Scenario",
            labels={
                "scenario": "Scenario",
                "revenue_per_mw_eur": "Revenue per MW (€)",
                "asset_id": "Asset",
            },
        )

        st.plotly_chart(fig_revenue_per_mw, use_container_width=True)

    with st.expander("View revenue scenario output table"):
        st.dataframe(filtered_revenue_df, use_container_width=True)


# ------------------------------------------------------------
# 4. Asset Product KPIs
# ------------------------------------------------------------

show_section_header(
    "4. Asset Product KPIs",
    "Asset-level product and commercial indicators combining revenue, customer usage, and product friction.",
)

if filtered_asset_kpis_df.empty:
    st.warning("No asset KPI data available for the selected filters.")
else:
    fig_opportunity = px.bar(
        filtered_asset_kpis_df.sort_values(
            "product_opportunity_score",
            ascending=False,
        ),
        x="asset_id",
        y="product_opportunity_score",
        color="product_opportunity_level",
        title="Product Opportunity Score by Asset",
        labels={
            "asset_id": "Asset",
            "product_opportunity_score": "Product Opportunity Score",
            "product_opportunity_level": "Opportunity Level",
        },
    )

    st.plotly_chart(fig_opportunity, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_health = px.bar(
            filtered_asset_kpis_df,
            x="asset_id",
            y="average_customer_health_score",
            color="asset_owner_type",
            title="Average Customer Health Score",
            labels={
                "asset_id": "Asset",
                "average_customer_health_score": "Customer Health Score",
                "asset_owner_type": "Asset Owner Type",
            },
        )
        st.plotly_chart(fig_health, use_container_width=True)

    with col2:
        fig_uplift = px.bar(
            filtered_asset_kpis_df,
            x="asset_id",
            y="revenue_uplift_vs_day_ahead_pct",
            color="best_scenario",
            title="Revenue Uplift vs Day-Ahead Baseline",
            labels={
                "asset_id": "Asset",
                "revenue_uplift_vs_day_ahead_pct": "Revenue Uplift (%)",
                "best_scenario": "Best Scenario",
            },
        )
        st.plotly_chart(fig_uplift, use_container_width=True)

    st.markdown("### Primary Product Need by Asset")

    product_need_table = filtered_asset_kpis_df[
        [
            "asset_id",
            "asset_name",
            "asset_owner_type",
            "best_scenario",
            "best_scenario_revenue_eur",
            "product_opportunity_score",
            "product_opportunity_level",
            "primary_product_need",
        ]
    ].sort_values("product_opportunity_score", ascending=False)

    st.dataframe(product_need_table, use_container_width=True)


# ------------------------------------------------------------
# 5. Grid Constraint Impact
# ------------------------------------------------------------

show_section_header(
    "5. Grid Constraint Impact",
    "How grid limitations translate into missed revenue and roadmap-relevant product needs.",
)

constraint_df = filtered_asset_kpis_df.copy()

if constraint_df.empty:
    st.warning("No grid-constraint KPI data available for selected assets.")
else:
    col1, col2 = st.columns(2)

    with col1:
        fig_missed = px.bar(
            constraint_df.sort_values("grid_missed_revenue_eur", ascending=False),
            x="asset_id",
            y="grid_missed_revenue_eur",
            color="asset_owner_type",
            title="Missed Revenue Due to Grid Constraints",
            labels={
                "asset_id": "Asset",
                "grid_missed_revenue_eur": "Missed Revenue (€)",
                "asset_owner_type": "Asset Owner Type",
            },
        )
        st.plotly_chart(fig_missed, use_container_width=True)

    with col2:
        fig_binding = px.bar(
            constraint_df.sort_values("grid_constraint_binding_hours", ascending=False),
            x="asset_id",
            y="grid_constraint_binding_hours",
            color="primary_product_need",
            title="Constraint-Binding Hours",
            labels={
                "asset_id": "Asset",
                "grid_constraint_binding_hours": "Hours",
                "primary_product_need": "Primary Product Need",
            },
        )
        st.plotly_chart(fig_binding, use_container_width=True)

    st.markdown(
        """
        Product interpretation:

        - High missed revenue suggests the product needs clearer grid-constraint explainability.
        - High constraint-binding hours suggest stronger operational alerting and customer-facing reporting.
        - Constraint-aware views help connect technical asset limitations with commercial expectations.
        """
    )


# ------------------------------------------------------------
# 6. Roadmap Prioritization
# ------------------------------------------------------------

show_section_header(
    "6. Roadmap Prioritization",
    "Feature prioritization using RICE-style product scoring.",
)

fig_roadmap = px.bar(
    roadmap_df.sort_values("rice_score", ascending=True),
    x="rice_score",
    y="feature",
    orientation="h",
    color="priority_level",
    title="Roadmap Priority Ranking",
    labels={
        "rice_score": "RICE Score",
        "feature": "Feature",
        "priority_level": "Priority Level",
    },
)

st.plotly_chart(fig_roadmap, use_container_width=True)

st.markdown("### Top Roadmap Priorities")

top_roadmap_table = roadmap_df[
    [
        "priority_rank",
        "feature",
        "priority_level",
        "rice_score",
        "target_user",
        "problem",
        "evidence_signal",
    ]
].sort_values("priority_rank")

st.dataframe(top_roadmap_table, use_container_width=True)

st.markdown(
    """
    Product interpretation:

    The roadmap is not based on generic feature ideas. It is linked to asset-level revenue,
    constraint signals, customer/product usage data, support burden, and commercial value.
    """
)


# ------------------------------------------------------------
# 7. V2 Roadmap
# ------------------------------------------------------------

show_section_header(
    "7. V2 Roadmap",
    "How this V1 product sprint can evolve into a more advanced product intelligence layer.",
)

v2_items = [
    {
        "V2 Area": "Real Market Data Integration",
        "Why it matters": "Move from synthetic sample data to DA, FCR, aFRR, intraday, and imbalance data.",
        "Product value": "Improves credibility and supports customer/investor discussions.",
    },
    {
        "V2 Area": "Optimization-Based Dispatch",
        "Why it matters": "Replace heuristic logic with SOC-constrained optimization.",
        "Product value": "Supports more realistic strategy comparison and engineering alignment.",
    },
    {
        "V2 Area": "Battery Degradation Logic",
        "Why it matters": "Revenue should be interpreted net of asset wear.",
        "Product value": "Improves trust with asset owners and investors.",
    },
    {
        "V2 Area": "Forecasting and Uncertainty",
        "Why it matters": "Market prices and revenues are uncertain.",
        "Product value": "Supports risk-aware product features and decision confidence.",
    },
    {
        "V2 Area": "Co-located PV + BESS View",
        "Why it matters": "Co-location creates shared grid-connection and curtailment challenges.",
        "Product value": "Supports renewable developers and hybrid asset owners.",
    },
    {
        "V2 Area": "Automated Customer Reporting",
        "Why it matters": "Customers need recurring explanations of value creation and missed value.",
        "Product value": "Reduces manual reporting and improves transparency.",
    },
    {
        "V2 Area": "Investor Revenue-Risk Dashboard",
        "Why it matters": "Investors need risk-adjusted revenue views before committing capital.",
        "Product value": "Supports commercial conversion and financing conversations.",
    },
]

v2_df = pd.DataFrame(v2_items)

st.dataframe(v2_df, use_container_width=True)

st.success(
    "V1 is designed as a focused, sendable product sprint. "
    "V2 extends the same concept with deeper market realism, optimization, and customer-facing reporting."
)


# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------

st.markdown("---")
st.caption(
    "BESS Product Intelligence Lab | Product Sprint V1 | "
    "Synthetic sample data for demonstration purposes."
)