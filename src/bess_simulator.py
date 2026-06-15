from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


# ============================================================
# BESS Product Intelligence Lab
# Step 3 - BESS Revenue Scenario Simulator
# ============================================================
#
# This module compares simple BESS revenue scenarios:
# 1. Day-Ahead only
# 2. FCR only
# 3. aFRR only
# 4. Day-Ahead + FCR
# 5. Day-Ahead + FCR + aFRR
# 6. Grid-constrained hybrid operation
#
# The purpose is product demonstration, not production trading.
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

MARKET_DATA_PATH = DATA_DIR / "sample_market_prices.csv"
ASSET_DATA_PATH = DATA_DIR / "sample_bess_assets.csv"
REVENUE_OUTPUT_PATH = OUTPUT_DIR / "revenue_scenarios.csv"


# ------------------------------------------------------------
# Loading and validation
# ------------------------------------------------------------

def load_input_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load market and asset datasets.
    """

    if not MARKET_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Market data not found: {MARKET_DATA_PATH}. "
            "Run python generate_sample_data.py first."
        )

    if not ASSET_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Asset data not found: {ASSET_DATA_PATH}. "
            "Run python generate_sample_data.py first."
        )

    market_df = pd.read_csv(MARKET_DATA_PATH)
    asset_df = pd.read_csv(ASSET_DATA_PATH)

    market_df["timestamp"] = pd.to_datetime(market_df["timestamp"])

    validate_market_data(market_df)
    validate_asset_data(asset_df)

    return market_df, asset_df


def validate_market_data(market_df: pd.DataFrame) -> None:
    """
    Validate market dataset columns.
    """

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

    if not market_df["grid_constraint_score"].between(0, 1).all():
        raise ValueError("grid_constraint_score must be between 0 and 1.")

    if not market_df["imbalance_risk_score"].between(0, 1).all():
        raise ValueError("imbalance_risk_score must be between 0 and 1.")


def validate_asset_data(asset_df: pd.DataFrame) -> None:
    """
    Validate BESS asset dataset columns.
    """

    required_columns = {
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

    missing_columns = required_columns - set(asset_df.columns)

    if missing_columns:
        raise ValueError(f"Missing asset columns: {missing_columns}")

    if asset_df.empty:
        raise ValueError("Asset dataframe is empty.")

    numeric_columns = [
        "power_mw",
        "energy_mwh",
        "round_trip_efficiency",
        "min_soc_mwh",
        "max_soc_mwh",
        "initial_soc_mwh",
        "grid_connection_mw",
    ]

    for col in numeric_columns:
        if (asset_df[col] < 0).any():
            raise ValueError(f"{col} must be non-negative.")

    if not asset_df["round_trip_efficiency"].between(0, 1).all():
        raise ValueError("round_trip_efficiency must be between 0 and 1.")


# ------------------------------------------------------------
# Utility helpers
# ------------------------------------------------------------

def get_asset_limits(asset: pd.Series) -> Dict[str, float]:
    """
    Extract useful BESS limits from one asset row.
    """

    power_mw = float(asset["power_mw"])
    energy_mwh = float(asset["energy_mwh"])
    grid_connection_mw = float(asset["grid_connection_mw"])

    usable_power_mw = min(power_mw, grid_connection_mw)

    return {
        "power_mw": power_mw,
        "energy_mwh": energy_mwh,
        "usable_power_mw": usable_power_mw,
        "grid_connection_mw": grid_connection_mw,
        "round_trip_efficiency": float(asset["round_trip_efficiency"]),
        "charge_efficiency": float(np.sqrt(asset["round_trip_efficiency"])),
        "discharge_efficiency": float(np.sqrt(asset["round_trip_efficiency"])),
        "min_soc_mwh": float(asset["min_soc_mwh"]),
        "max_soc_mwh": float(asset["max_soc_mwh"]),
        "initial_soc_mwh": float(asset["initial_soc_mwh"]),
    }


def calculate_product_recommendation(
    scenario_name: str,
    total_revenue_eur: float,
    missed_revenue_eur: float,
    constraint_binding_hours: int,
    dominant_market: str,
) -> str:
    """
    Translate technical outputs into a product recommendation.

    This is intentionally product-oriented. The objective is to show how a PM can
    connect model outputs to product roadmap decisions.
    """

    if constraint_binding_hours >= 20 or missed_revenue_eur > 0.10 * max(total_revenue_eur, 1):
        return "Prioritize Grid Constraint Explainability"

    if dominant_market == "day_ahead" and scenario_name != "Day-Ahead Only":
        return "Add Market Diversification View"

    if dominant_market in {"fcr", "afrr"}:
        return "Add Revenue Attribution by Reserve Market"

    if "Hybrid" in scenario_name:
        return "Build Customer-Facing Strategy Comparison"

    return "Create Monthly Revenue Explanation Report"


def calculate_market_shares(
    day_ahead_revenue_eur: float,
    fcr_revenue_eur: float,
    afrr_revenue_eur: float,
) -> Dict[str, float]:
    """
    Calculate market revenue shares.
    """

    total_market_revenue = (
        max(day_ahead_revenue_eur, 0)
        + max(fcr_revenue_eur, 0)
        + max(afrr_revenue_eur, 0)
    )

    if total_market_revenue <= 0:
        return {
            "market_share_day_ahead_pct": 0.0,
            "market_share_fcr_pct": 0.0,
            "market_share_afrr_pct": 0.0,
            "dominant_market": "none",
        }

    shares = {
        "market_share_day_ahead_pct": round(
            100 * max(day_ahead_revenue_eur, 0) / total_market_revenue, 2
        ),
        "market_share_fcr_pct": round(
            100 * max(fcr_revenue_eur, 0) / total_market_revenue, 2
        ),
        "market_share_afrr_pct": round(
            100 * max(afrr_revenue_eur, 0) / total_market_revenue, 2
        ),
    }

    dominant_market = max(
        {
            "day_ahead": shares["market_share_day_ahead_pct"],
            "fcr": shares["market_share_fcr_pct"],
            "afrr": shares["market_share_afrr_pct"],
        },
        key={
            "day_ahead": shares["market_share_day_ahead_pct"],
            "fcr": shares["market_share_fcr_pct"],
            "afrr": shares["market_share_afrr_pct"],
        }.get,
    )

    shares["dominant_market"] = dominant_market

    return shares


# ------------------------------------------------------------
# Scenario 1 - Day-Ahead arbitrage
# ------------------------------------------------------------

def simulate_day_ahead_arbitrage(
    market_df: pd.DataFrame,
    asset: pd.Series,
    power_multiplier: float = 1.0,
    apply_grid_constraints: bool = False,
) -> Dict[str, float]:
    """
    Simulate a simple Day-Ahead arbitrage strategy.

    Logic:
    - Charge during low-price hours
    - Discharge during high-price hours
    - Respect SOC, power, and grid connection constraints
    - Optionally reduce available grid power during constrained hours

    This is a heuristic, not a full optimizer.
    """

    limits = get_asset_limits(asset)

    prices = market_df["day_ahead_price_eur_mwh"].to_numpy()
    grid_constraint_score = market_df["grid_constraint_score"].to_numpy()

    low_price_threshold = np.quantile(prices, 0.30)
    high_price_threshold = np.quantile(prices, 0.70)

    soc = limits["initial_soc_mwh"]

    charge_eff = limits["charge_efficiency"]
    discharge_eff = limits["discharge_efficiency"]

    base_power_limit = limits["usable_power_mw"] * power_multiplier

    total_charge_mwh = 0.0
    total_discharge_mwh = 0.0

    charge_cost_eur = 0.0
    discharge_revenue_eur = 0.0

    constraint_binding_hours = 0
    missed_revenue_eur = 0.0

    for i, price in enumerate(prices):
        constraint_score = grid_constraint_score[i]

        if apply_grid_constraints:
            available_power_mw = base_power_limit * (1 - 0.60 * constraint_score)
            available_power_mw = max(available_power_mw, 0)
        else:
            available_power_mw = base_power_limit

        if available_power_mw < base_power_limit * 0.95:
            constraint_binding_hours += 1

        # Charge during low-price hours.
        if price <= low_price_threshold:
            max_charge_from_power = available_power_mw
            remaining_soc_room = limits["max_soc_mwh"] - soc

            # Energy bought from market, accounting for charging efficiency.
            market_energy_to_charge_mwh = min(
                max_charge_from_power,
                remaining_soc_room / max(charge_eff, 1e-6),
            )

            if market_energy_to_charge_mwh > 0:
                soc += market_energy_to_charge_mwh * charge_eff
                total_charge_mwh += market_energy_to_charge_mwh
                charge_cost_eur += market_energy_to_charge_mwh * price

        # Discharge during high-price hours.
        elif price >= high_price_threshold:
            max_discharge_from_power = available_power_mw
            available_soc_energy = soc - limits["min_soc_mwh"]

            battery_energy_to_discharge_mwh = min(
                max_discharge_from_power / max(discharge_eff, 1e-6),
                available_soc_energy,
            )

            market_energy_sold_mwh = battery_energy_to_discharge_mwh * discharge_eff

            if market_energy_sold_mwh > 0:
                soc -= battery_energy_to_discharge_mwh
                total_discharge_mwh += market_energy_sold_mwh
                discharge_revenue_eur += market_energy_sold_mwh * price

                if apply_grid_constraints and constraint_score > 0.3:
                    unconstrained_possible_power = base_power_limit
                    constrained_power_loss = max(
                        unconstrained_possible_power - available_power_mw,
                        0,
                    )
                    missed_revenue_eur += constrained_power_loss * price * 0.15

    net_revenue_eur = discharge_revenue_eur - charge_cost_eur

    return {
        "day_ahead_revenue_eur": round(net_revenue_eur, 2),
        "fcr_revenue_eur": 0.0,
        "afrr_revenue_eur": 0.0,
        "total_revenue_eur": round(net_revenue_eur, 2),
        "total_charge_mwh": round(total_charge_mwh, 2),
        "total_discharge_mwh": round(total_discharge_mwh, 2),
        "constraint_binding_hours": int(constraint_binding_hours),
        "missed_revenue_eur": round(missed_revenue_eur, 2),
    }


# ------------------------------------------------------------
# Scenario 2 - FCR capacity revenue
# ------------------------------------------------------------

def simulate_fcr_revenue(
    market_df: pd.DataFrame,
    asset: pd.Series,
    reserve_multiplier: float = 0.45,
    apply_grid_constraints: bool = False,
) -> Dict[str, float]:
    """
    Simulate FCR capacity revenue.

    Logic:
    - A share of BESS power is reserved for FCR
    - Capacity revenue is earned every hour
    - Grid constraints reduce available capacity if activated
    """

    limits = get_asset_limits(asset)

    fcr_prices = market_df["fcr_price_eur_mw_h"].to_numpy()
    grid_constraint_score = market_df["grid_constraint_score"].to_numpy()

    base_reserve_mw = limits["usable_power_mw"] * reserve_multiplier

    total_fcr_revenue = 0.0
    total_reserved_mw_h = 0.0
    constraint_binding_hours = 0
    missed_revenue_eur = 0.0

    for i, price in enumerate(fcr_prices):
        constraint_score = grid_constraint_score[i]

        if apply_grid_constraints:
            available_reserve_mw = base_reserve_mw * (1 - 0.40 * constraint_score)
            available_reserve_mw = max(available_reserve_mw, 0)
        else:
            available_reserve_mw = base_reserve_mw

        if available_reserve_mw < base_reserve_mw * 0.95:
            constraint_binding_hours += 1
            missed_revenue_eur += (base_reserve_mw - available_reserve_mw) * price

        total_fcr_revenue += available_reserve_mw * price
        total_reserved_mw_h += available_reserve_mw

    return {
        "day_ahead_revenue_eur": 0.0,
        "fcr_revenue_eur": round(total_fcr_revenue, 2),
        "afrr_revenue_eur": 0.0,
        "total_revenue_eur": round(total_fcr_revenue, 2),
        "total_charge_mwh": 0.0,
        "total_discharge_mwh": 0.0,
        "total_reserved_mw_h": round(total_reserved_mw_h, 2),
        "constraint_binding_hours": int(constraint_binding_hours),
        "missed_revenue_eur": round(missed_revenue_eur, 2),
    }


# ------------------------------------------------------------
# Scenario 3 - aFRR capacity revenue
# ------------------------------------------------------------

def simulate_afrr_revenue(
    market_df: pd.DataFrame,
    asset: pd.Series,
    up_multiplier: float = 0.30,
    down_multiplier: float = 0.25,
    apply_grid_constraints: bool = False,
) -> Dict[str, float]:
    """
    Simulate aFRR up/down capacity revenue.

    Logic:
    - A share of BESS power is reserved for upward aFRR
    - A share of BESS power is reserved for downward aFRR
    - Revenue is based on synthetic capacity prices
    - Grid constraints reduce available reserve capacity if activated
    """

    limits = get_asset_limits(asset)

    afrr_up_prices = market_df["afrr_up_price_eur_mw_h"].to_numpy()
    afrr_down_prices = market_df["afrr_down_price_eur_mw_h"].to_numpy()
    grid_constraint_score = market_df["grid_constraint_score"].to_numpy()

    base_up_mw = limits["usable_power_mw"] * up_multiplier
    base_down_mw = limits["usable_power_mw"] * down_multiplier

    total_afrr_revenue = 0.0
    total_reserved_mw_h = 0.0
    constraint_binding_hours = 0
    missed_revenue_eur = 0.0

    for i in range(len(market_df)):
        constraint_score = grid_constraint_score[i]

        if apply_grid_constraints:
            available_up_mw = base_up_mw * (1 - 0.45 * constraint_score)
            available_down_mw = base_down_mw * (1 - 0.35 * constraint_score)
        else:
            available_up_mw = base_up_mw
            available_down_mw = base_down_mw

        available_up_mw = max(available_up_mw, 0)
        available_down_mw = max(available_down_mw, 0)

        if (
            available_up_mw < base_up_mw * 0.95
            or available_down_mw < base_down_mw * 0.95
        ):
            constraint_binding_hours += 1
            missed_revenue_eur += (
                (base_up_mw - available_up_mw) * afrr_up_prices[i]
                + (base_down_mw - available_down_mw) * afrr_down_prices[i]
            )

        hourly_revenue = (
            available_up_mw * afrr_up_prices[i]
            + available_down_mw * afrr_down_prices[i]
        )

        total_afrr_revenue += hourly_revenue
        total_reserved_mw_h += available_up_mw + available_down_mw

    return {
        "day_ahead_revenue_eur": 0.0,
        "fcr_revenue_eur": 0.0,
        "afrr_revenue_eur": round(total_afrr_revenue, 2),
        "total_revenue_eur": round(total_afrr_revenue, 2),
        "total_charge_mwh": 0.0,
        "total_discharge_mwh": 0.0,
        "total_reserved_mw_h": round(total_reserved_mw_h, 2),
        "constraint_binding_hours": int(constraint_binding_hours),
        "missed_revenue_eur": round(missed_revenue_eur, 2),
    }


# ------------------------------------------------------------
# Hybrid scenarios
# ------------------------------------------------------------

def simulate_hybrid_da_fcr(
    market_df: pd.DataFrame,
    asset: pd.Series,
    apply_grid_constraints: bool = False,
) -> Dict[str, float]:
    """
    Simulate a hybrid Day-Ahead + FCR strategy.

    Product interpretation:
    The BESS combines energy arbitrage with reserve capacity revenue.
    """

    da_result = simulate_day_ahead_arbitrage(
        market_df=market_df,
        asset=asset,
        power_multiplier=0.55,
        apply_grid_constraints=apply_grid_constraints,
    )

    fcr_result = simulate_fcr_revenue(
        market_df=market_df,
        asset=asset,
        reserve_multiplier=0.35,
        apply_grid_constraints=apply_grid_constraints,
    )

    result = {
        "day_ahead_revenue_eur": da_result["day_ahead_revenue_eur"],
        "fcr_revenue_eur": fcr_result["fcr_revenue_eur"],
        "afrr_revenue_eur": 0.0,
        "total_revenue_eur": round(
            da_result["day_ahead_revenue_eur"] + fcr_result["fcr_revenue_eur"],
            2,
        ),
        "total_charge_mwh": da_result["total_charge_mwh"],
        "total_discharge_mwh": da_result["total_discharge_mwh"],
        "total_reserved_mw_h": fcr_result["total_reserved_mw_h"],
        "constraint_binding_hours": int(
            max(
                da_result["constraint_binding_hours"],
                fcr_result["constraint_binding_hours"],
            )
        ),
        "missed_revenue_eur": round(
            da_result["missed_revenue_eur"] + fcr_result["missed_revenue_eur"],
            2,
        ),
    }

    return result


def simulate_hybrid_da_fcr_afrr(
    market_df: pd.DataFrame,
    asset: pd.Series,
    apply_grid_constraints: bool = False,
) -> Dict[str, float]:
    """
    Simulate a hybrid Day-Ahead + FCR + aFRR strategy.

    Product interpretation:
    The BESS participates in multiple value pools, creating a need for
    explainability, revenue attribution, and strategy comparison.
    """

    da_result = simulate_day_ahead_arbitrage(
        market_df=market_df,
        asset=asset,
        power_multiplier=0.45,
        apply_grid_constraints=apply_grid_constraints,
    )

    fcr_result = simulate_fcr_revenue(
        market_df=market_df,
        asset=asset,
        reserve_multiplier=0.25,
        apply_grid_constraints=apply_grid_constraints,
    )

    afrr_result = simulate_afrr_revenue(
        market_df=market_df,
        asset=asset,
        up_multiplier=0.18,
        down_multiplier=0.15,
        apply_grid_constraints=apply_grid_constraints,
    )

    result = {
        "day_ahead_revenue_eur": da_result["day_ahead_revenue_eur"],
        "fcr_revenue_eur": fcr_result["fcr_revenue_eur"],
        "afrr_revenue_eur": afrr_result["afrr_revenue_eur"],
        "total_revenue_eur": round(
            da_result["day_ahead_revenue_eur"]
            + fcr_result["fcr_revenue_eur"]
            + afrr_result["afrr_revenue_eur"],
            2,
        ),
        "total_charge_mwh": da_result["total_charge_mwh"],
        "total_discharge_mwh": da_result["total_discharge_mwh"],
        "total_reserved_mw_h": round(
            fcr_result["total_reserved_mw_h"]
            + afrr_result["total_reserved_mw_h"],
            2,
        ),
        "constraint_binding_hours": int(
            max(
                da_result["constraint_binding_hours"],
                fcr_result["constraint_binding_hours"],
                afrr_result["constraint_binding_hours"],
            )
        ),
        "missed_revenue_eur": round(
            da_result["missed_revenue_eur"]
            + fcr_result["missed_revenue_eur"]
            + afrr_result["missed_revenue_eur"],
            2,
        ),
    }

    return result


# ------------------------------------------------------------
# Run all scenarios
# ------------------------------------------------------------

def build_scenario_record(
    asset: pd.Series,
    scenario_name: str,
    scenario_result: Dict[str, float],
) -> Dict[str, object]:
    """
    Convert scenario outputs into one clean row for the final output table.
    """

    market_shares = calculate_market_shares(
        day_ahead_revenue_eur=scenario_result.get("day_ahead_revenue_eur", 0.0),
        fcr_revenue_eur=scenario_result.get("fcr_revenue_eur", 0.0),
        afrr_revenue_eur=scenario_result.get("afrr_revenue_eur", 0.0),
    )

    total_revenue_eur = scenario_result.get("total_revenue_eur", 0.0)
    missed_revenue_eur = scenario_result.get("missed_revenue_eur", 0.0)
    constraint_binding_hours = scenario_result.get("constraint_binding_hours", 0)

    recommendation = calculate_product_recommendation(
        scenario_name=scenario_name,
        total_revenue_eur=total_revenue_eur,
        missed_revenue_eur=missed_revenue_eur,
        constraint_binding_hours=constraint_binding_hours,
        dominant_market=market_shares["dominant_market"],
    )

    power_mw = float(asset["power_mw"])
    energy_mwh = float(asset["energy_mwh"])

    return {
        "asset_id": asset["asset_id"],
        "asset_name": asset["asset_name"],
        "country": asset["country"],
        "asset_owner_type": asset["asset_owner_type"],
        "commercial_model": asset["commercial_model"],
        "scenario": scenario_name,
        "day_ahead_revenue_eur": scenario_result.get("day_ahead_revenue_eur", 0.0),
        "fcr_revenue_eur": scenario_result.get("fcr_revenue_eur", 0.0),
        "afrr_revenue_eur": scenario_result.get("afrr_revenue_eur", 0.0),
        "total_revenue_eur": total_revenue_eur,
        "revenue_per_mw_eur": round(total_revenue_eur / max(power_mw, 1e-6), 2),
        "revenue_per_mwh_eur": round(total_revenue_eur / max(energy_mwh, 1e-6), 2),
        "total_charge_mwh": scenario_result.get("total_charge_mwh", 0.0),
        "total_discharge_mwh": scenario_result.get("total_discharge_mwh", 0.0),
        "total_reserved_mw_h": scenario_result.get("total_reserved_mw_h", 0.0),
        "constraint_binding_hours": constraint_binding_hours,
        "missed_revenue_eur": missed_revenue_eur,
        "market_share_day_ahead_pct": market_shares["market_share_day_ahead_pct"],
        "market_share_fcr_pct": market_shares["market_share_fcr_pct"],
        "market_share_afrr_pct": market_shares["market_share_afrr_pct"],
        "dominant_market": market_shares["dominant_market"],
        "product_recommendation": recommendation,
    }


def run_scenarios_for_asset(
    market_df: pd.DataFrame,
    asset: pd.Series,
) -> List[Dict[str, object]]:
    """
    Run all V1 scenarios for one BESS asset.
    """

    scenario_outputs = []

    scenario_map = {
        "Day-Ahead Only": simulate_day_ahead_arbitrage(
            market_df=market_df,
            asset=asset,
            power_multiplier=1.0,
            apply_grid_constraints=False,
        ),
        "FCR Only": simulate_fcr_revenue(
            market_df=market_df,
            asset=asset,
            reserve_multiplier=0.55,
            apply_grid_constraints=False,
        ),
        "aFRR Only": simulate_afrr_revenue(
            market_df=market_df,
            asset=asset,
            up_multiplier=0.35,
            down_multiplier=0.30,
            apply_grid_constraints=False,
        ),
        "Hybrid DA + FCR": simulate_hybrid_da_fcr(
            market_df=market_df,
            asset=asset,
            apply_grid_constraints=False,
        ),
        "Hybrid DA + FCR + aFRR": simulate_hybrid_da_fcr_afrr(
            market_df=market_df,
            asset=asset,
            apply_grid_constraints=False,
        ),
        "Grid-Constrained Hybrid": simulate_hybrid_da_fcr_afrr(
            market_df=market_df,
            asset=asset,
            apply_grid_constraints=True,
        ),
    }

    for scenario_name, scenario_result in scenario_map.items():
        scenario_outputs.append(
            build_scenario_record(
                asset=asset,
                scenario_name=scenario_name,
                scenario_result=scenario_result,
            )
        )

    return scenario_outputs


def run_all_scenarios() -> pd.DataFrame:
    """
    Run all scenarios for all BESS assets and save the result.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    market_df, asset_df = load_input_data()

    all_records = []

    for _, asset in asset_df.iterrows():
        asset_records = run_scenarios_for_asset(
            market_df=market_df,
            asset=asset,
        )
        all_records.extend(asset_records)

    revenue_df = pd.DataFrame(all_records)

    revenue_df = revenue_df.sort_values(
        by=["asset_id", "total_revenue_eur"],
        ascending=[True, False],
    )

    revenue_df.to_csv(REVENUE_OUTPUT_PATH, index=False)

    return revenue_df


def print_summary(revenue_df: pd.DataFrame) -> None:
    """
    Print a simple terminal summary.
    """

    print("BESS revenue scenarios generated successfully.")
    print(f"Output saved to: {REVENUE_OUTPUT_PATH}")
    print()
    print(f"Rows generated: {len(revenue_df)}")
    print(f"Assets: {revenue_df['asset_id'].nunique()}")
    print(f"Scenarios: {revenue_df['scenario'].nunique()}")
    print()

    print("Top scenario per asset:")
    top_scenarios = (
        revenue_df.sort_values("total_revenue_eur", ascending=False)
        .groupby("asset_id")
        .head(1)
    )

    for _, row in top_scenarios.iterrows():
        print(
            f"- {row['asset_id']} | {row['scenario']} | "
            f"{row['total_revenue_eur']:.2f} EUR | "
            f"Recommendation: {row['product_recommendation']}"
        )

    print()
    print("Scenario revenue summary:")
    scenario_summary = (
        revenue_df.groupby("scenario")["total_revenue_eur"]
        .mean()
        .sort_values(ascending=False)
    )

    for scenario, value in scenario_summary.items():
        print(f"- {scenario}: {value:.2f} EUR average")


if __name__ == "__main__":
    results_df = run_all_scenarios()
    print_summary(results_df)