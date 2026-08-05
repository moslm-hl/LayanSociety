import sys
import numpy as np
from scipy.stats import linregress
from datetime import datetime

from logger_config import get_application_logger, setup_statement_logger

from tunisia_inflation_calculator import (
    calculate_inflation,
    INFLATION_RATES,
    sanitize_filename,
    get_username,
    get_account_number,
    _write_statement_header,
    _write_client_information,
    _write_statement_footer,
)

# Module logger
logger = get_application_logger('estimator')


def _configure_console_output():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    logger.info("Console configured for UTF-8 output")

ENVIRONMENTAL_SURCHARGES = {
    "water": {"label": "Water & irrigation costs", "rate": 0.045},
    "energy": {"label": "Energy & fuel costs", "rate": 0.035},
    "food": {"label": "Food & agriculture costs", "rate": 0.055},
    "construction": {"label": "Construction & housing costs", "rate": 0.028},
    "transport": {"label": "Transport & logistics costs", "rate": 0.022},
    "healthcare": {"label": "Healthcare costs", "rate": 0.032},
    "education": {"label": "Education costs", "rate": 0.018},
    "general": {"label": "General cost of living", "rate": 0.000},
}


def _compute_scenarios():
    years = np.array(list(range(2021, 2027)), dtype=float)
    rates = np.array([INFLATION_RATES[int(y)] for y in years], dtype=float)

    base_avg = float(np.mean(rates))
    trend_slope = float(linregress(years, rates).slope)

    return {
        "optimistic": base_avg * 0.65,
        "baseline": base_avg + trend_slope,
        "pessimistic": base_avg * 1.45,
    }


SCENARIOS = _compute_scenarios()


def estimate_future_cost(
    amount: float,
    base_year: int,
    target_year: int,
    category: str = "general",
    scenario: str = "baseline",
) -> dict:
    """Estimate future cost adjusted for inflation trend and sector surcharge."""
    logger.debug(f"Estimating future cost: {amount} TND from {base_year} to {target_year}, category: {category}, scenario: {scenario}")

    adjusted_2026 = calculate_inflation(amount, base_year)

    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario}")

    if category not in ENVIRONMENTAL_SURCHARGES:
        raise ValueError(f"Unknown category: {category}")

    years_projected = target_year - 2026
    if years_projected < 1:
        raise ValueError("target_year must be >= 2027")

    surcharge_rate = ENVIRONMENTAL_SURCHARGES[category]["rate"]
    annual_rate = (SCENARIOS[scenario] / 100.0) + surcharge_rate

    projected = adjusted_2026 * ((1 + annual_rate) ** years_projected)

    result = {
        "original_amount": amount,
        "base_year": base_year,
        "adjusted_2026": adjusted_2026,
        "projected": projected,
        "total_multiplier": round(projected / amount, 4),
        "annual_rate_used": round(annual_rate * 100, 4),
        "years_projected": years_projected,
        "category": category,
        "scenario": scenario,
        "target_year": target_year,
    }
    logger.debug(f"Future cost estimation result: {projected:.2f} TND")
    return result


def _prompt_amount():
    logger.info("Prompting for amount")
    while True:
        try:
            amount = float(input("Enter the main amount in Tunisian Dinars (TND), e.g. 1000: "))
            if amount <= 0:
                print("Amount must be greater than 0. Please try again.")
                logger.warning("User entered invalid amount (<= 0)")
                continue
            logger.info(f"Amount entered: {amount} TND")
            return amount
        except ValueError:
            print("Invalid amount. Please enter a number (example: 1000 or 1000.50).")
            logger.warning("User entered invalid amount format")


def _prompt_base_year():
    logger.info("Prompting for base year")
    while True:
        try:
            year = int(input("Enter the ORIGINAL year of that amount (2010-2026): "))
            if year < 2010 or year > 2026:
                print("Year must be between 2010 and 2026. Please try again.")
                logger.warning(f"User entered invalid base year: {year}")
                continue
            logger.info(f"Base year entered: {year}")
            return year
        except ValueError:
            print("Invalid year. Please enter a 4-digit year (example: 2020).")
            logger.warning("User entered invalid year format")


def _prompt_target_year():
    logger.info("Prompting for target year")
    while True:
        try:
            year = int(input("Enter the FUTURE year to project to (2027-2040): "))
            if year < 2027 or year > 2040:
                print("Year must be between 2027 and 2040. Please try again.")
                logger.warning(f"User entered invalid target year: {year}")
                continue
            logger.info(f"Target year entered: {year}")
            return year
        except ValueError:
            print("Invalid year. Please enter a 4-digit year (example: 2030).")
            logger.warning("User entered invalid year format")


def _prompt_category():
    logger.info("Prompting for cost category")
    categories = list(ENVIRONMENTAL_SURCHARGES.keys())

    print("\nSelect a cost category:")
    for index, key in enumerate(categories, 1):
        label = ENVIRONMENTAL_SURCHARGES[key]["label"]
        rate_pct = ENVIRONMENTAL_SURCHARGES[key]["rate"] * 100
        print(f"{index}. {label} (+{rate_pct:.1f}%)")

    while True:
        choice = input("Enter the category number: ").strip()
        try:
            idx = int(choice)
            if idx < 1 or idx > len(categories):
                print("Please choose a valid category number from the list.")
                logger.warning(f"User entered invalid category number: {choice}")
                continue
            selected = categories[idx - 1]
            logger.info(f"Category selected: {selected}")
            return selected
        except ValueError:
            print("Invalid input. Please enter a number from the list.")
            logger.warning("User entered invalid category format")


def _format_money(value: float) -> str:
    return f"{value:,.2f} TND"


def _build_projection_rows(amount: float, base_year: int, target_year: int, category: str):
    scenarios = [
        ("Optimistic", "optimistic"),
        ("Baseline", "baseline"),
        ("Pessimistic", "pessimistic"),
    ]

    rows = []
    for label, key in scenarios:
        result = estimate_future_cost(
            amount=amount,
            base_year=base_year,
            target_year=target_year,
            category=category,
            scenario=key,
        )
        annual_rate_str = f"{result['annual_rate_used']:.1f}%"
        projected_str = _format_money(result["projected"])
        multiplier_str = f"{result['total_multiplier']:.2f}x"
        rows.append((label, annual_rate_str, projected_str, multiplier_str, result))

    return rows


def _print_projection_table(rows):
    # 76 chars wide
    top = "╔" + "═" * 74 + "╗"
    title = "║" + "         FUTURE COST PROJECTION — Tunisia (TND)".ljust(74) + "║"
    sep1 = "╠" + "═" * 18 + "╦" + "═" * 14 + "╦" + "═" * 15 + "╦" + "═" * 25 + "╣"
    header = (
        "║" + " Scenario".ljust(18)
        + "║" + " Annual Rate".ljust(14)
        + "║" + " Projected".ljust(15)
        + "║" + " Multiplier".ljust(25)
        + "║"
    )
    sep2 = sep1
    bottom = "╚" + "═" * 18 + "╩" + "═" * 14 + "╩" + "═" * 15 + "╩" + "═" * 25 + "╝"

    print(top)
    print(title)
    print(sep1)
    print(header)
    print(sep2)

    for scenario_label, annual_rate_str, projected_str, multiplier_str, _ in rows:
        line = (
            "║" + f" {scenario_label}".ljust(18)
            + "║" + f" {annual_rate_str}".ljust(14)
            + "║" + f" {projected_str}".ljust(15)
            + "║" + f" {multiplier_str}".ljust(25)
            + "║"
        )
        print(line)

    print(bottom)


def _write_projection_log(log_file_path: str, username: str, account_number: str, rows, amount: float, base_year: int, target_year: int, category: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%d/%m/%Y")

    with open(log_file_path, "a", encoding="utf-8") as log_file:
        _write_statement_header(log_file, date_str)
        _write_client_information(log_file, username, account_number, timestamp)

        log_file.write("FUTURE COST PROJECTION\n")
        log_file.write("-" * 76 + "\n")
        log_file.write(f"{'Original Amount:':<20} {amount:>15,.2f} TND\n")
        log_file.write(f"{'Base Year:':<20} {base_year:>15}\n")
        log_file.write(f"{'Target Year:':<20} {target_year:>15}\n")
        log_file.write(f"{'Category:':<20} {ENVIRONMENTAL_SURCHARGES[category]['label']}\n\n")

        log_file.write(f"{'Scenario':<15} {'Annual Rate':<15} {'Projected':<25} {'Multiplier':<15}\n")
        log_file.write("-" * 76 + "\n")

        for scenario_label, annual_rate_str, projected_str, multiplier_str, _ in rows:
            log_file.write(
                f"{scenario_label:<15} {annual_rate_str:<15} {projected_str:<25} {multiplier_str:<15}\n"
            )

        log_file.write("\n")
        _write_statement_footer(log_file)


def main():
    logger.info("Future cost estimator started")
    _configure_console_output()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        logger.info("Running in test mode")
        amount = 1000.0
        base_year = 2020
        target_year = 2035
        category = "general"
        rows = _build_projection_rows(amount, base_year, target_year, category)
        _print_projection_table(rows)
        return

    try:
        print("=== Tunisia Future Cost Estimator (2027-2040) ===")
        print()

        username = get_username()
        account_number = get_account_number()
        logger.info(f"User: {username}, Account: {account_number or 'N/A'}")

        amount = _prompt_amount()
        base_year = _prompt_base_year()
        category = _prompt_category()
        target_year = _prompt_target_year()

        rows = _build_projection_rows(amount, base_year, target_year, category)
        _print_projection_table(rows)

        safe_user = sanitize_filename(username)
        date_part = datetime.now().strftime("%Y%m%d")
        time_part = datetime.now().strftime("%H%M%S")
        log_file_path = f"future_log_{safe_user}_{date_part}_{time_part}.log"
        _write_projection_log(log_file_path, username, account_number, rows, amount, base_year, target_year, category)

        print(f"\nResults saved to: {log_file_path}")
        logger.info(f"Future cost estimation completed. Results saved to: {log_file_path}")

    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
        print("\n\nProgram interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        print(f"\nAn error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
