# Customer and User Personas

## Purpose

This document defines the main external and internal users considered in the BESS Product Intelligence Lab V1 prototype.

The goal is to show how battery-storage product features can be connected to real user needs, customer pain points, business value, and product KPIs.

---

# 1. Battery Asset Owner

## Role

Owns or operates one or more grid-scale BESS assets and wants to maximize commercial value.

## Main Goals

* Maximize revenue
* Understand market participation
* Reduce revenue uncertainty
* Monitor asset performance
* Understand missed value
* Trust the optimization strategy

## Pain Points

* Revenue results can be difficult to explain
* It is not always clear which market created value
* Grid constraints can reduce performance
* Asset owners need clear monthly reporting
* The customer may not understand why a hybrid strategy outperforms a simple strategy

## Product Questions

* Which market created most of my revenue?
* Why did my battery underperform in certain hours?
* How much revenue did I lose because of constraints?
* Should I focus on DA, FCR, aFRR, or a hybrid strategy?
* How is my asset performing compared with expectations?

## Needed Features

* Revenue attribution engine
* Market strategy comparison
* Grid-constraint explainability
* Monthly customer report
* Missed-revenue explanation
* Asset performance dashboard

## Success Metrics

* Revenue per MW
* Revenue uplift vs baseline
* Missed revenue due to constraints
* Report downloads
* Customer health score
* Reduction in support tickets

---

# 2. Project Developer

## Role

Develops new BESS projects and needs to assess revenue potential, commercial models, and technical limitations before investment or project execution.

## Main Goals

* Evaluate project feasibility
* Understand market-revenue potential
* Compare commercial strategies
* Prepare investor discussions
* Understand grid-connection limitations
* Support go/no-go decisions

## Pain Points

* Difficulty comparing revenue strategies
* Uncertainty around grid-connection constraints
* Need to explain revenue assumptions to investors
* Lack of clear product views for early-stage project assessment

## Product Questions

* What is the expected revenue range for this asset?
* Which market strategy is most attractive?
* How sensitive is revenue to grid constraints?
* How does the grid connection limit affect value?
* Which product features can help make the project bankable?

## Needed Features

* Scenario explorer
* Grid-connection sensitivity analysis
* Revenue-risk comparison
* Investor-ready summary report
* Co-location analysis for PV + BESS projects

## Success Metrics

* Time needed to compare strategies
* Revenue uplift across scenarios
* Constraint-binding hours
* Investor report usage
* Project conversion rate

---

# 3. Infrastructure Investor

## Role

Provides capital for BESS assets and needs confidence in commercial performance, revenue stability, and risk exposure.

## Main Goals

* Understand risk-adjusted revenue
* Compare merchant and protected-revenue models
* Evaluate asset bankability
* Assess downside risk
* Receive clear and credible reporting

## Pain Points

* Merchant revenue can be volatile
* Technical outputs may not be investor-friendly
* It is difficult to understand which constraints affect returns
* Investors need clear comparison between revenue models

## Product Questions

* What is the expected revenue range?
* Which share of revenue comes from each market?
* What is the downside risk?
* What happens if grid constraints reduce availability?
* How does a floor-style revenue model compare to merchant exposure?

## Needed Features

* Investor risk dashboard
* Revenue attribution
* Floor-style revenue comparison
* Monthly executive report
* Missed-revenue explanation
* Scenario-based revenue ranges

## Success Metrics

* Investor report usage
* Revenue stability index
* Forecast/revenue deviation
* Customer health score
* Commercial conversion rate

---

# 4. Renewable Developer / IPP

## Role

Develops or owns renewable assets and may add BESS for co-location, curtailment reduction, grid-supportive operation, or market participation.

## Main Goals

* Improve renewable asset value
* Reduce curtailment
* Use shared grid connection efficiently
* Stack value across markets
* Understand PV + BESS operational logic

## Pain Points

* Shared grid connections create complexity
* Curtailment and export limits are difficult to monetize
* It is not always clear when BESS should charge from PV or the grid
* Co-location products require clear operational explanations

## Product Questions

* How does BESS improve my renewable project?
* How much curtailment can be reduced?
* How does the grid connection affect revenue?
* Should the battery prioritize market trading or renewable smoothing?
* Which operational strategy supports the best commercial result?

## Needed Features

* Co-location view
* Grid-connection limit visualization
* Curtailment-reduction module
* Market strategy explorer
* Revenue attribution by source
* Customer reporting

## Success Metrics

* Curtailment reduction
* Incremental BESS revenue
* Grid-constraint hours
* Revenue per MW
* Customer engagement
* Project expansion rate

---

# 5. Municipal Utility

## Role

Owns or operates local energy infrastructure and may use BESS for flexibility, reliability, grid support, and market participation.

## Main Goals

* Improve local grid performance
* Support flexibility needs
* Reduce congestion impact
* Create additional revenue
* Maintain operational reliability

## Pain Points

* Municipal utilities may be more risk-sensitive
* They need explainable operation
* Grid constraints and local flexibility needs can be difficult to connect with market revenues
* Product outputs must be understandable to non-trading stakeholders

## Product Questions

* How does the BESS support the local grid?
* What value comes from market participation?
* Does revenue conflict with grid-supportive operation?
* How can missed revenue or constrained operation be explained?
* Which alerts are needed for operations?

## Needed Features

* Grid-support mode
* Constraint explainability
* Operational alerts
* Local flexibility reporting
* Simple executive dashboard
* Customer-facing monthly report

## Success Metrics

* Constraint-binding hours
* Missed revenue explained
* Asset availability
* Alert response time
* Report engagement
* Support-ticket reduction

---

# 6. Internal Trader / Portfolio Manager

## Role

Uses the product to understand market allocation, revenue performance, strategy behavior, and portfolio-level opportunities.

## Main Goals

* Maximize portfolio revenue
* Understand market allocation
* Identify underperforming assets
* Detect operational limitations
* Support strategy adjustment

## Pain Points

* Multi-market revenue can become difficult to interpret
* Manual analysis creates operational burden
* Strategy comparison requires clean data and visual explanation
* Grid constraints can affect trading decisions

## Product Questions

* Which assets are underperforming?
* Which markets generated revenue?
* Which assets are constrained?
* Where should strategy be adjusted?
* Which product features would reduce manual work?

## Needed Features

* Portfolio dashboard
* Market allocation view
* Revenue attribution
* Constraint and missed-revenue alerts
* Strategy comparison
* Product health scoring

## Success Metrics

* Revenue uplift
* Optimizer success rate
* Manual override count
* Missed-revenue reduction
* Portfolio revenue per MW
* Operational alert accuracy

---

# 7. Customer Success / Sales Team

## Role

Uses product outputs to explain value to customers, support renewals, reduce confusion, and support commercial conversations.

## Main Goals

* Explain customer value clearly
* Reduce support burden
* Improve customer trust
* Support upsell and renewal conversations
* Translate technical results into business language

## Pain Points

* Customers may not understand why revenue changes
* Support teams need simple explanations
* Manual reporting consumes time
* Sales teams need credible product evidence

## Product Questions

* What value did the product create for this customer?
* Why did revenue change this month?
* Which feature would improve the customer experience?
* Which customers are at risk?
* What should be included in the monthly report?

## Needed Features

* Monthly customer report generator
* Revenue explanation layer
* Customer health score
* Product opportunity score
* Roadmap-linked customer pain points
* Exportable charts and summaries

## Success Metrics

* Support tickets
* Report downloads
* Dashboard views
* Customer health score
* Renewal support
* Sales enablement usage

---

# Persona Summary

| Persona                             | Main Need                         | Key Product Feature                  |
| ----------------------------------- | --------------------------------- | ------------------------------------ |
| Battery Asset Owner                 | Understand and maximize revenue   | Revenue Attribution Engine           |
| Project Developer                   | Compare project strategies        | Market Strategy Scenario Explorer    |
| Infrastructure Investor             | Assess risk and bankability       | Investor Risk Dashboard              |
| Renewable Developer / IPP           | Evaluate co-location value        | Co-location View                     |
| Municipal Utility                   | Connect BESS with grid support    | Grid Constraint Explainability       |
| Internal Trader / Portfolio Manager | Improve market strategy decisions | Portfolio and Market Allocation View |
| Customer Success / Sales            | Explain value to customers        | Monthly Customer Report Generator    |

---

# Product Insight

The same technical battery data has different meanings for different users.

A strong BESS product should not only calculate revenue. It should translate revenue, constraints, risk, and operational signals into the language of each stakeholder.
