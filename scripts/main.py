#!/usr/bin/env python3
import sys
from datetime import datetime

# Add parent directory to path to import core modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.logger_config import setup_logger, setup_statement_logger, get_application_logger

from core.tunisia_inflation_calculator import (
    calculate_inflation,
    log_calculation,
    get_username,
    get_account_number,
    generate_log_filename,
    _write_statement_header,
    _write_client_information,
    _write_statement_footer,
    sanitize_filename,
    _total_adjusted_additional_costs,
)

from core.tunisia_future_cost_estimator import (
    estimate_future_cost,
    ENVIRONMENTAL_SURCHARGES,
)

# Application logger
logger = get_application_logger('main')


SOCIETY_NAME = "LAYAN SOCIETY FOR COST CALCULATION AND RISK ESTIMATION"
WIDTH = 76


def setup_console():
    """Configure console for UTF-8 output."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    logger.info("Console configured for UTF-8 output")


def print_banner(title: str):
    """Print society banner with title."""
    border = "=" * WIDTH
    print(f"\n{border}")
    print(f"{SOCIETY_NAME:^76}")
    print(f"{title:^76}")
    print(f"{border}\n")
    logger.info(f"Displaying banner: {title}")


def _run_inflation_demo(username: str, account_number: str):
    """Run inflation calculator demo with banner."""
    logger.info(f"Starting inflation demo for user: {username}")
    print_banner("INFLATION ADJUSTMENT CALCULATOR")
    
    amount = 1000.0
    base_year = 2020
    additional_costs = [{"amount": 120.0, "year": 2022}]

    adjusted_amount = calculate_inflation(amount, base_year)
    total_additional_adjusted = _total_adjusted_additional_costs(additional_costs)
    grand_total = adjusted_amount + total_additional_adjusted

    log_file_path = generate_log_filename(username)
    log_calculation(
        log_file_path,
        username,
        account_number,
        amount,
        base_year,
        adjusted_amount,
        additional_costs,
        grand_total,
    )
    
    print(f"Results: {amount:,.2f} TND ({base_year}) → {adjusted_amount:,.2f} TND (2026)")
    print(f"Log saved: {log_file_path}")
    logger.info(f"Inflation calculation completed. Log saved to: {log_file_path}")

    return log_file_path


def _write_future_projection_log(
    log_file_path: str,
    username: str,
    account_number: str,
    amount: float,
    base_year: int,
    target_year: int,
    category: str,
):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%d/%m/%Y")

    scenarios = [
        ("Optimistic", "optimistic"),
        ("Baseline", "baseline"),
        ("Pessimistic", "pessimistic"),
    ]

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

        for label, scenario_key in scenarios:
            result = estimate_future_cost(
                amount=amount,
                base_year=base_year,
                target_year=target_year,
                category=category,
                scenario=scenario_key,
            )
            annual_rate_str = f"{result['annual_rate_used']:.1f}%"
            projected_str = f"{result['projected']:,.2f} TND"
            multiplier_str = f"{result['total_multiplier']:.2f}x"
            log_file.write(
                f"{label:<15} {annual_rate_str:<15} {projected_str:<25} {multiplier_str:<15}\n"
            )

        log_file.write("\n")
        _write_statement_footer(log_file)


def _run_project_test():
    """Run combined project test with banners."""
    logger.info("Starting project test mode")
    setup_console()
    
    print_banner("PROJECT TEST MODE")
    
    username = "TEST_USER"
    account_number = "TEST-0001"

    inflation_log = _run_inflation_demo(username, account_number)

    safe_user = sanitize_filename(username)
    date_part = datetime.now().strftime("%Y%m%d")
    time_part = datetime.now().strftime("%H%M%S")
    project_log = f"project_test_log_{safe_user}_{date_part}_{time_part}.log"

    # Use statement logger for project test log
    statement_logger = setup_statement_logger(username)
    statement_logger.info("PROJECT TEST LOG")
    statement_logger.info("=" * 76)
    statement_logger.info(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    statement_logger.info(f"Inflation statement: {inflation_log}")

    _write_future_projection_log(
        project_log,
        username,
        account_number,
        amount=1000.0,
        base_year=2020,
        target_year=2035,
        category="general",
    )
    
    print(f"\nTest completed!")
    print(f"  Inflation log: {inflation_log}")
    print(f"  Project log: {project_log}")
    logger.info(f"Project test completed. Inflation log: {inflation_log}, Project log: {project_log}")

    return project_log


def main():
    """Main entry point with menu."""
    logger.info("Application started")
    setup_console()

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        logger.info("Running in test mode")
        log_path = _run_project_test()
        return

    while True:
        print("\n" + "=" * 76)
        print(f"{SOCIETY_NAME:^76}")
        print("=" * 76)
        print("\n  1. Inflation Calculator (Historical: 2010-2026)")
        print("  2. Future Cost Estimator (Projections: 2027-2040)")
        print("  3. GDP Projection Calculator")
        print("  4. Unemployment Rate Calculator")
        print("  5. Currency Converter (TND/USD/EUR)")
        print("  6. Interest Rate Impact Calculator")
        print("  7. Run Project Test")
        print("  8. Exit")
        print("-" * 76)
        
        choice = input("Enter choice(s) (1-8, separate multiple with spaces): ").strip()

        # Parse multiple choices
        choices = choice.split()
        
        for choice in choices:
            if choice == "1":
                logger.info("User selected Inflation Calculator")
                print_banner("INFLATION ADJUSTMENT CALCULATOR")
                import tunisia_inflation_calculator as calc
                calc.main()
            elif choice == "2":
                logger.info("User selected Future Cost Estimator")
                print_banner("FUTURE COST ESTIMATOR")
                import tunisia_future_cost_estimator as future
                future.main()
            elif choice == "3":
                logger.info("User selected GDP Projection Calculator")
                print_banner("GDP PROJECTION CALCULATOR")
                import gdp_calculator as gdp
                gdp.main()
            elif choice == "4":
                logger.info("User selected Unemployment Rate Calculator")
                print_banner("UNEMPLOYMENT RATE CALCULATOR")
                import unemployment_calculator as unemp
                unemp.main()
            elif choice == "5":
                logger.info("User selected Currency Converter")
                print_banner("CURRENCY CONVERTER")
                import currency_converter as currency
                currency.main()
            elif choice == "6":
                logger.info("User selected Interest Rate Impact Calculator")
                print_banner("INTEREST RATE IMPACT CALCULATOR")
                import interest_calculator as interest
                interest.main()
            elif choice == "7":
                logger.info("User selected Project Test")
                log_path = _run_project_test()
                input("\nPress Enter to continue...")
            elif choice == "8":
                logger.info("User exited application")
                print(f"\nThank you for using {SOCIETY_NAME}")
                return
            else:
                logger.warning(f"Invalid menu choice: {choice}")
                print(f"Invalid choice: {choice}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
        print("\n\nProgram interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        print(f"\nAn error occurred: {e}")
        sys.exit(1)
