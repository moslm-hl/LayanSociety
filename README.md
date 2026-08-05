# LAYAN SOCIETY FOR COST CALCULATION AND RISK ESTIMATION

## Tunisia Economic Analysis Tools

A comprehensive Python project for calculating historical inflation adjustments and projecting future costs in Tunisia. This toolset helps individuals and organizations understand purchasing power changes and plan for future expenses based on economic trends.

---

## Features

### Inflation Calculator (2010-2026)
- Calculate inflation-adjusted amounts from any year between 2010-2026
- Handles multiple additional costs with individual year inputs
- Generates personalized bank-statement-style log files
- Shows purchasing power loss percentage and value multipliers
- Supports user identity and account number tracking

### Future Cost Estimator (2027-2040)
- Projects future costs based on historical inflation trends
- Three scenarios: Optimistic, Baseline, and Pessimistic
- Category-based surcharges (Energy, Food, Healthcare, General)
- Uses numpy and scipy for trend analysis and linear regression
- Detailed scenario comparison tables

### Project-Wide Features
- Centralized entry point via `main.py`
- Professional society branding on all outputs
- UTF-8 console and log file support
- Clean, modular architecture with clear function names
- Test mode for validation without user input

---

## Project Structure

```
Economy/
├── main.py                          # Central entry point with menu
├── tunisia_inflation_calculator.py  # Historical inflation (2010-2026)
├── tunisia_future_cost_estimator.py # Future projections (2027-2040)
└── README.md                        # This file
```

---

## Installation

### Requirements
- Python 3.8 or higher
- numpy
- scipy

### Setup
```bash
pip install numpy scipy
```

---

## Usage

### Main Entry Point (Recommended)

Run the project menu to access all tools:

```bash
python main.py
```

Menu options:
1. **Inflation Calculator** - Calculate historical adjustments (2010-2026)
2. **Future Cost Estimator** - Project future costs (2027-2040)
3. **Run Project Test** - Automated test with sample data
4. **Exit** - Close the application

### Direct Script Execution

#### Inflation Calculator
```bash
# Interactive mode
python tunisia_inflation_calculator.py

# Test mode
python tunisia_inflation_calculator.py --test
```

#### Future Cost Estimator
```bash
# Interactive mode
python tunisia_future_cost_estimator.py

# Test mode
python tunisia_future_cost_estimator.py --test
```

#### Project Test (Combined)
```bash
python main.py --test
```

---

## Example Outputs

### Inflation Calculator Example
```
=== Tunisia Money Inflation Calculator (2010-2026) ===

Enter your name: MOSLM
Enter an account/reference number: 1200
Your statement will be saved to: log_moslm_20260325_201128.log

Enter the main amount in Tunisian Dinars (TND), e.g. 1000: 5000
Enter the year of that amount (2010-2026): 2020
Do you want to add additional costs (y/n)? y

Enter additional costs (type 'done' when finished):
Enter cost amount in TND (or 'done' to finish): 1200
Enter the year for this cost (1200.0 TND) (2010-2026): 2022
Added: 1200.0 TND from 2022

Enter cost amount in TND (or 'done' to finish): done

============================================================
CALCULATION RESULTS
============================================================
Original Amount (TND): 5,000.00
Original Year: 2020
Inflation-Adjusted Amount (2026): 7,641.75

Additional Costs (inflation-adjusted to 2026):
--------------------------------------------------
  Cost 1: 1,200.00 TND from 2022 -> 1,368.48 TND (2026)

Total Additional Costs (2026): 1,368.48

Grand Total (2026): 9,010.23

Purchasing Power Loss (main amount): 52.8%
Value Multiplier (main amount): 1.53x

Results saved to: log_moslm_20260325_201128.log
```

### Future Cost Estimator Example
```
=== Tunisia Future Cost Estimator (2027-2040) ===

Enter your name: MOSLM
Enter an account/reference number (optional): 1200
Enter the main amount in Tunisian Dinars (TND): 2030
Enter the ORIGINAL year of that amount (2010-2026): 2020

Select a category for cost projection:
  1. energy
  2. food
  3. healthcare
  4. general

Enter category number (1-4): 4
Enter the FUTURE year to project to (2027-2040): 2030

FUTURE COST PROJECTION (2026 → 2030)
--------------------------------------------------------------------------------
Original Amount:            2,030.00 TND (in 2020)
Adjusted to 2026:           3,102.43 TND
Target Year:                    2030
Category:            General cost of living

Scenario        Annual Rate     Projected                 Multiplier
--------------------------------------------------------------------------------
Optimistic      4.8%            3,741.12 TND              1.84x
Baseline        7.4%            4,133.47 TND              2.04x
Pessimistic     10.6%           4,626.94 TND              2.28x

Results saved to: future_log_moslm_20260325_201128.log
```

---

## Inflation Data

### Historical Rates (2010-2026)
| Year | Rate | Year | Rate |
|------|------|------|------|
| 2010 | 4.4% | 2019 | 6.7% |
| 2011 | 3.2% | 2020 | 5.6% |
| 2012 | 4.6% | 2021 | 5.7% |
| 2013 | 5.3% | 2022 | 8.3% |
| 2014 | 4.6% | 2023 | 9.3% |
| 2015 | 4.4% | 2024 | 7.0% |
| 2016 | 3.6% | 2025 | 5.9% |
| 2017 | 5.3% | 2026 | 7.8% |
| 2018 | 7.3% |      |      |

### Future Projection Scenarios (2027-2040)
| Scenario | Base Rate | Description |
|----------|-----------|-------------|
| Optimistic | ~4.8% | Low inflation with economic stability |
| Baseline | ~7.4% | Moderate inflation based on recent trends |
| Pessimistic | ~10.6% | High inflation with economic challenges |

### Category Surcharges
| Category | Surcharge | Description |
|----------|-----------|-------------|
| Energy | +2.5% | Higher volatility in energy prices |
| Food | +1.8% | Agricultural and supply chain factors |
| Healthcare | +1.5% | Medical cost inflation |
| General | 0% | Standard cost of living |

---

## Log Files

All calculations generate professional log files:
- **Inflation logs**: `log_{username}_{date}_{time}.log`
- **Future logs**: `future_log_{username}_{date}_{time}.log`
- **Test logs**: `project_test_log_{username}_{date}_{time}.log`

Each log includes:
- Society header and branding
- Client information (name, account number, date)
- Detailed calculations with breakdowns
- Financial summaries with percentages
- Professional formatting with signatures

---

## Test Mode

Run tests to validate calculations without manual input:

```bash
# Test individual components
python tunisia_inflation_calculator.py --test
python tunisia_future_cost_estimator.py --test

# Test entire project
python main.py --test
```

Test results are automatically logged and displayed.

---

## Technical Details

### Architecture
- **Modular design**: Separate scripts for different calculators
- **Clean imports**: Explicit function imports, no circular dependencies
- **Type hints**: Function signatures include return types
- **Error handling**: KeyboardInterrupt and general exception handling
- **Console encoding**: UTF-8 support for international characters

### Key Functions

#### Inflation Calculator
- `calculate_inflation(amount, start_year, end_year)` - Core inflation calculation
- `generate_log_filename(username)` - Create unique log filenames
- `log_calculation(...)` - Save results to log file
- `get_positive_float(prompt)` - Robust input validation
- `get_year_in_range(prompt, min, max)` - Year validation

#### Future Estimator
- `estimate_future_cost(amount, base_year, target_year, category, scenario)` - Future projection
- `compute_trend_rate()` - Linear regression on historical data
- `_prompt_base_year()` - Get historical year (2010-2026)
- `_prompt_target_year()` - Get future year (2027-2040)

---

## Disclaimer

- Inflation rates are approximate annual percentages
- Future projections are estimates based on historical trends
- This tool is for informational purposes only
- For official transactions, consult with financial institutions
- The LAYAN SOCIETY FOR COST CALCULATION AND RISK ESTIMATION provides this as an educational tool

---

## Author

**LAYAN SOCIETY FOR COST CALCULATION AND RISK ESTIMATION**

Developed for economic analysis and educational purposes in Tunisia.

---

## License

This project is provided as-is for educational and informational use.

---

## Support

For issues or questions:
1. Check the test mode output: `python main.py --test`
2. Verify Python version: `python --version` (requires 3.8+)
3. Ensure dependencies are installed: `pip install numpy scipy`

---

**Last Updated**: March 2026  
**Version**: 2.0  
**Compatible with**: Python 3.8+
