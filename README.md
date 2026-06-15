# BESS Product Intelligence Lab

## Product Sprint V1

This project is a compact product sprint demonstrating how battery storage market intelligence, revenue scenario analysis, product KPIs, and roadmap prioritization can support grid-scale BESS software decisions.

The goal is not to replicate a production trading platform. The goal is to show how a Senior Product Manager can translate energy-market complexity into product requirements, customer value, software features, and measurable product outcomes.

---

## Why This Project Exists

Grid-scale battery storage owners, developers, investors, and operators need more than dispatch optimization. They need to understand:

* Where battery revenues come from
* Which market strategies create the most value
* How grid constraints reduce revenue
* How product features can improve transparency and trust
* Which roadmap items should be prioritized based on customer and business value

This project connects technical BESS logic with product thinking.

---

## What V1 Demonstrates

V1 focuses on speed, clarity, and product relevance.

It demonstrates:

* Product discovery
* Customer and user understanding
* Battery storage market logic
* Revenue scenario comparison
* Grid-constraint impact analysis
* Product KPI design
* Roadmap prioritization
* Technical feasibility through a simple Python/Streamlit prototype

---

## V1 Scope

The V1 prototype includes:

1. Sample market data for battery revenue scenarios
2. Sample BESS asset data
3. Sample product-usage data
4. Revenue scenario simulator
5. Product KPI framework
6. Streamlit dashboard
7. Product brief
8. Customer personas
9. Product Requirements Document
10. Roadmap prioritization
11. V2 roadmap

---

## V1 Scenarios

The prototype compares several battery operation scenarios:

1. Day-Ahead only
2. FCR only
3. aFRR only
4. Day-Ahead + FCR
5. Day-Ahead + FCR + aFRR
6. Grid-constrained hybrid operation

The purpose is not to provide production-grade optimization, but to show how scenario logic can support product decisions.

---

## Product Questions Answered

This project is designed to answer product-management questions such as:

1. Which battery strategy creates the most customer value?
2. Which market contributes most to revenue?
3. Where is value lost because of grid constraints?
4. Which product feature should be prioritized next?
5. Which KPIs should the product team track?
6. How can technical outputs be translated into customer-facing explanations?

---

## Target Users

The product thinking in this project considers multiple users:

* Battery asset owners
* Project developers
* Infrastructure investors
* Independent power producers
* Municipal utilities
* Internal trading teams
* Operations teams
* Sales and customer-success teams
* Product and engineering teams

---

## Repository Structure

```text
bess-product-intelligence-lab/
│
├── README.md
├── requirements.txt
├── app.py
├── generate_sample_data.py
├── .gitignore
│
├── data/
│   ├── sample_market_prices.csv
│   ├── sample_bess_assets.csv
│   └── sample_product_usage.csv
│
├── src/
│   ├── bess_simulator.py
│   ├── market_metrics.py
│   └── product_kpis.py
│
├── outputs/
│   ├── revenue_scenarios.csv
│   ├── asset_kpis.csv
│   └── roadmap_prioritization.csv
│
├── product/
│   ├── 01_product_brief.md
│   ├── 02_customer_personas.md
│   ├── 03_prd.md
│   ├── 04_product_kpi_framework.md
│   ├── 05_roadmap_prioritization.md
│   └── 06_v2_roadmap.md
│
└── demo/
    ├── demo_script.md
    └── screenshots/
```

---

## V1 Sample Data

V1 uses synthetic sample data for demonstration purposes. The data is designed to support product thinking and prototype development, not to represent actual trading results.

The generated datasets are:

| File                            | Purpose                                                                                                     |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `data/sample_market_prices.csv` | Synthetic market signals for Day-Ahead, FCR, aFRR, grid constraints, and imbalance risk                     |
| `data/sample_bess_assets.csv`   | Sample BESS assets with power, energy, efficiency, SOC limits, grid connection limits, and commercial model |
| `data/sample_product_usage.csv` | Sample customer/product usage data for product KPI analysis                                                 |

To generate the sample data:

```bash
python generate_sample_data.py
```

---

## Revenue Scenario Simulator

The V1 simulator compares multiple battery operation strategies across the sample BESS assets.

Run the simulator:

```bash
python src/bess_simulator.py
```

This creates:

```text
outputs/revenue_scenarios.csv
```

The output includes:

* Total revenue by asset and scenario
* Revenue per MW
* Revenue per MWh
* Day-Ahead, FCR, and aFRR revenue shares
* Constraint-binding hours
* Missed revenue due to grid constraints
* Product recommendation linked to each scenario

---

## How to Run the Full V1 Workflow

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate sample data:

```bash
python generate_sample_data.py
```

Run the revenue scenario simulator:

```bash
python src/bess_simulator.py
```

Run the Streamlit dashboard:

```bash
streamlit run app.py
```

---

## Current V1 Outputs

| Output                          | Description                                    |
| ------------------------------- | ---------------------------------------------- |
| `data/sample_market_prices.csv` | Synthetic hourly market data                   |
| `data/sample_bess_assets.csv`   | Sample BESS asset portfolio                    |
| `data/sample_product_usage.csv` | Product usage and customer health data         |
| `outputs/revenue_scenarios.csv` | Revenue scenario comparison across BESS assets |

Additional outputs will be added in the next steps:

| Planned Output                       | Description                                        |
| ------------------------------------ | -------------------------------------------------- |
| `outputs/asset_kpis.csv`             | Asset-level product and commercial KPIs            |
| `outputs/roadmap_prioritization.csv` | Feature prioritization using product scoring logic |

---

## Product Interpretation

The simulator is designed to connect technical outputs with product decisions.

Examples:

| Technical Signal                                   | Product Interpretation                                 |
| -------------------------------------------------- | ------------------------------------------------------ |
| High missed revenue due to constraints             | Need for Grid Constraint Explainability                |
| Revenue concentrated in one market                 | Need for Market Diversification View                   |
| High reserve-market revenue                        | Need for Revenue Attribution by Reserve Market         |
| High constraint-binding hours                      | Need for Operational Alerting and Customer Explanation |
| Hybrid strategy outperforms single-market strategy | Need for Customer-Facing Strategy Comparison           |

This is the core product-management logic of V1: technical results are not only calculated; they are translated into roadmap-relevant product insights.

---

## Product Management Relevance

This project demonstrates the ability to:

* Frame customer problems
* Translate technical complexity into product requirements
* Define product KPIs
* Prioritize features using structured logic
* Build a lightweight prototype
* Communicate across technical, commercial, and strategic stakeholders
* Connect energy-market knowledge with software-product decisions

---

## V2 Roadmap

V1 is intentionally compact. V2 will increase market realism, technical depth, and product maturity.

Planned V2 improvements:

* Real market data integration
* Optimization-based BESS dispatch
* Battery degradation-aware operation
* Forecasting and uncertainty module
* Intraday and imbalance logic
* Co-located PV + BESS use case
* Grid-constraint explainability
* Investor-facing revenue-risk dashboard
* Automated customer reporting
* API-ready architecture

---

## V1 vs V2 Logic

V1 is designed as a focused, sendable portfolio artifact. It prioritizes clarity, product thinking, and fast execution.

V2 will extend the prototype into a more advanced product intelligence layer with stronger technical realism, market data integration, and customer-facing reporting.

| Version | Purpose                                                                                                                |
| ------- | ---------------------------------------------------------------------------------------------------------------------- |
| V1      | Demonstrate product thinking, BESS scenario logic, KPIs, roadmap prioritization, and technical feasibility             |
| V2      | Add real-market data, optimization depth, degradation logic, forecasting, co-location, and investor/customer reporting |

---

## Status

Current version: V1 product sprint.

V1 is designed to be clear, compact, and application-ready. V2 will build on this foundation after the initial application is sent.
