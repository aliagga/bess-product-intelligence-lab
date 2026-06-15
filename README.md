# BESS Product Intelligence Lab

## Product Sprint V1

This project is a compact product sprint demonstrating how battery storage market intelligence, revenue scenario analysis, product KPIs, and roadmap prioritization can support grid-scale BESS software decisions.

The goal is not to replicate a production trading platform. The goal is to show how a Senior Product Manager can translate energy-market complexity into product requirements, customer value, software features, and measurable product outcomes.

---

## Why This Project Exists

Grid-scale battery storage owners, developers, investors, and operators need more than dispatch optimization. They need to understand:

- Where battery revenues come from
- Which market strategies create the most value
- How grid constraints reduce revenue
- How product features can improve transparency and trust
- Which roadmap items should be prioritized based on customer and business value

This project connects technical BESS logic with product thinking.

---

## What V1 Demonstrates

V1 focuses on speed, clarity, and product relevance.

It demonstrates:

- Product discovery
- Customer and user understanding
- Battery storage market logic
- Revenue scenario comparison
- Grid-constraint impact analysis
- Product KPI design
- Roadmap prioritization
- Technical feasibility through a simple Python/Streamlit prototype

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

- Battery asset owners
- Project developers
- Infrastructure investors
- Independent power producers
- Municipal utilities
- Internal trading teams
- Operations teams
- Sales and customer-success teams
- Product and engineering teams

---

## Repository Structure

```text
bess-product-intelligence-lab/
│
├── README.md
├── requirements.txt
├── app.py
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