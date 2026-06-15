# Product Requirements Document

## Product Name

BESS Product Intelligence Layer

## Prototype Name

BESS Product Intelligence Lab — V1

---

## Document Purpose

This PRD defines the V1 product requirements for a compact product-intelligence prototype for grid-scale battery storage software.

The goal is to show how market signals, BESS revenue scenarios, product usage data, asset KPIs, and roadmap prioritization can be combined into a product layer that supports customer value, internal decision-making, and product strategy.

---

## Background

Grid-scale battery storage software products must help customers and internal teams understand complex revenue and operational behavior.

Battery assets can create value through multiple markets, including Day-Ahead arbitrage, reserve markets such as FCR, aFRR, future intraday opportunities, imbalance management, and other flexibility services.

However, optimized dispatch alone is not enough. Customers also need to understand:

* Which markets created revenue
* Why revenue changed
* What constraints reduced value
* Which strategy performed best
* Whether the product is working reliably
* Which next features would improve value or trust

This creates a need for a product-intelligence layer that connects technical optimization outputs with customer-facing explanations and roadmap decisions.

---

## Product Objectives

The V1 product objectives are:

1. Compare BESS revenue scenarios across multiple market strategies.
2. Translate market and asset results into product-facing KPIs.
3. Identify missed revenue caused by grid constraints.
4. Combine technical and product-usage signals into asset-level product insights.
5. Prioritize roadmap features using structured product logic.
6. Communicate results through a simple dashboard and product documentation.
7. Define a clear V2 roadmap for a more advanced version.

---

## Users

### External Users

* Battery asset owners
* Project developers
* Infrastructure investors
* Renewable developers
* Independent power producers
* Municipal utilities

### Internal Users

* Product managers
* Trading teams
* Optimization/data-science teams
* Operations teams
* Sales teams
* Customer-success teams
* Leadership teams

---

## User Stories

### Asset Owner

As a battery asset owner, I want to understand which market created my revenue so that I can trust the optimization strategy.

### Investor

As an infrastructure investor, I want to compare merchant and protected-revenue scenarios so that I can evaluate risk-adjusted returns.

### Project Developer

As a project developer, I want to compare BESS strategies before investment so that I can understand the commercial potential of the asset.

### Renewable Developer

As a renewable developer, I want to understand how grid constraints and co-location affect battery value so that I can design better hybrid projects.

### Trader / Portfolio Manager

As a trader or portfolio manager, I want to see revenue attribution and strategy performance so that I can identify where market strategy should be adjusted.

### Operations Team

As an operations user, I want to identify constraint-binding hours and missed revenue so that I can explain operational limitations.

### Customer Success

As a customer-success user, I want a clear monthly explanation of revenue and missed value so that I can reduce support tickets and improve customer trust.

### Product Manager

As a product manager, I want to connect technical signals with product KPIs and roadmap priorities so that feature decisions are based on evidence.

---

## V1 Functional Requirements

### FR1 — Load Market Data

The system shall load synthetic hourly market data including:

* Day-Ahead price
* FCR price
* aFRR up price
* aFRR down price
* Grid constraint score
* Imbalance risk score

### FR2 — Load BESS Asset Data

The system shall load sample BESS asset data including:

* Asset ID
* Country
* Power rating
* Energy capacity
* Efficiency
* SOC limits
* Grid connection limit
* Commercial model
* Asset owner type

### FR3 — Simulate Revenue Scenarios

The system shall simulate the following V1 scenarios:

1. Day-Ahead only
2. FCR only
3. aFRR only
4. Day-Ahead + FCR
5. Day-Ahead + FCR + aFRR
6. Grid-constrained hybrid operation

### FR4 — Calculate Revenue Metrics

The system shall calculate:

* Total revenue
* Revenue per MW
* Revenue per MWh
* Day-Ahead revenue
* FCR revenue
* aFRR revenue
* Market revenue shares
* Dominant market

### FR5 — Calculate Grid Constraint Impact

The system shall calculate:

* Constraint-binding hours
* Missed revenue due to grid constraints
* Constraint-related product recommendation

### FR6 — Calculate Market Metrics

The system shall calculate product-facing market metrics including:

* Average Day-Ahead price
* Minimum and maximum Day-Ahead price
* Average daily Day-Ahead spread
* High-price hours
* Low-price hours
* Negative-price hours
* Average FCR price
* Average aFRR up/down prices
* High grid-constraint hours
* High imbalance-risk hours

### FR7 — Calculate Asset-Level Product KPIs

The system shall calculate:

* Best revenue scenario
* Best scenario revenue
* Revenue uplift vs Day-Ahead baseline
* Grid missed revenue
* Customer health score
* Product opportunity score
* Product opportunity level
* Primary product need

### FR8 — Prioritize Roadmap Features

The system shall prioritize roadmap features using RICE-style scoring:

* Reach
* Impact
* Confidence
* Effort
* RICE score
* Priority rank
* Priority level

### FR9 — Display Dashboard

The system shall display a Streamlit dashboard with:

1. Executive overview
2. Market intelligence
3. Revenue scenario comparison
4. Asset product KPIs
5. Grid constraint impact
6. Roadmap prioritization
7. V2 roadmap

### FR10 — Provide Product Documentation

The repository shall include:

* Product brief
* Customer personas
* PRD
* Product KPI framework
* Roadmap prioritization explanation
* V2 roadmap

---

## V1 Non-Functional Requirements

### NFR1 — Clarity

The dashboard and documentation should be understandable to product, commercial, and technical stakeholders.

### NFR2 — Reproducibility

The full workflow should be reproducible through simple commands:

```bash
python generate_sample_data.py
python src/bess_simulator.py
python src/market_metrics.py
python src/product_kpis.py
streamlit run app.py
```

### NFR3 — Modularity

The code should be organized into separate modules for:

* Data generation
* BESS simulation
* Market metrics
* Product KPIs
* Dashboard

### NFR4 — Transparency

The prototype should clearly state that V1 uses synthetic data and simplified revenue logic.

### NFR5 — Extensibility

The structure should support future V2 additions such as:

* Real market data
* Optimization-based dispatch
* Degradation modeling
* Forecasting
* Co-location
* Customer reporting
* API-ready architecture

---

## V1 Success Metrics

The V1 sprint is successful if it produces:

| Success Area          | Metric                                                             |
| --------------------- | ------------------------------------------------------------------ |
| Technical feasibility | All scripts run successfully                                       |
| Product clarity       | Dashboard clearly explains revenue, constraints, KPIs, and roadmap |
| Customer relevance    | Personas and product brief map technical outputs to user needs     |
| Product requirements  | PRD defines clear functional and non-functional requirements       |
| Roadmap logic         | Features are prioritized using evidence-based scoring              |
| Sendability           | The repo can be shared as a portfolio artifact                     |
| Extensibility         | V2 roadmap is clear and credible                                   |

---

## V1 Limitations

V1 is intentionally simplified.

Current limitations:

* Synthetic sample data
* Heuristic revenue simulation
* No full optimization model
* No real trading logic
* No degradation cost
* No forecasting model
* No intraday market
* No imbalance settlement
* No real customer data
* No production deployment

These limitations are intentional because V1 focuses on product clarity, rapid execution, and portfolio demonstration.

---

## V2 Product Direction

V2 should extend V1 by adding:

1. Real market data integration
2. Optimization-based BESS dispatch
3. Battery degradation-aware operation
4. Forecasting and uncertainty
5. Intraday and imbalance logic
6. Co-located PV + BESS use case
7. Customer monthly reporting
8. Investor revenue-risk dashboard
9. API-ready architecture
10. More advanced product analytics

---

## Product Hypothesis

If battery asset owners, investors, and internal teams can clearly understand how value is created, where value is lost, and which constraints affect performance, then customer trust, product adoption, commercial conversion, and roadmap quality improve.

---

## Product Principle

The product should not only optimize battery operation. It should explain battery value.
