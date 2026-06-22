# Dynamic Pricing Engine for Service-Based Businesses 🚀

## Overview
This project optimizes business profitability by implementing an **AI-driven Dynamic Pricing Engine**. By leveraging historical demand patterns and price elasticity, the system dynamically adjusts service prices to maximize revenue during peak times and ensure high capacity utilization during low-demand periods.

## The Problem
Service-based businesses often suffer from fixed pricing, leading to two major inefficiencies:
1. **Lost Revenue:** Charging base prices during peak demand (e.g., summer, holidays).
2. **Idle Capacity:** Failing to attract customers during low-demand periods.

## Key Results
* **Profit Uplift:** Successfully increased annual revenue by **16.79%** through dynamic pricing.
* **Model Performance:** Achieved 75% accuracy in predicting conversion probability (`was_booked`).
* **Data-Driven Strategy:** Implemented a pricing elasticity logic that automatically adapts to market shocks.

## Tech Stack
* **Language:** Python
* **ML Library:** XGBoost
* **Data manipulation:** Pandas, NumPy
* **Visualization:** Matplotlib

## How to use
1. Run `dynamic_pricing.ipynb` to train the model.
2. Use the `get_prediction()` function to get real-time price recommendations based on your current business demand.