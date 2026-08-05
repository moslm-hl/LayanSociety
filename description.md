# Economy Project Description

This project is a small Python toolkit for Tunisia economic analysis.

## Purpose
- Calculate inflation-adjusted values for historical amounts (2010–2026)
- Project future costs for 2027–2040 using inflation trends and category surcharges

## Main Components
- `main.py`: menu-driven entry point for inflation calculation, future projection, and test mode
- `tunisia_inflation_calculator.py`: historical inflation calculator with log file generation
- `tunisia_future_cost_estimator.py`: future cost estimator using optimistic, baseline, and pessimistic scenarios

## Features
- Interactive console input for name, account number, amount, years, and category
- Generates text logs for calculation results
- Uses official Tunisia inflation rates and estimated future inflation scenarios
- Supports multiple categories such as energy, food, healthcare, construction, and general costs
