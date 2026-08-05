#!/usr/bin/env python3
"""
GDP Projection Calculator
Projects GDP growth based on historical data and different scenarios.
"""

import sys
import os
from datetime import datetime

# Add parent directory to path to import core modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.logger_config import get_application_logger, setup_statement_logger
from core.tunisia_economic_indicators import (
    calculate_gdp_projection,
    get_economic_summary,
    GDP_GROWTH_RATES,
)
from core.tunisia_inflation_calculator import (
    sanitize_filename,
    get_username,
    get_account_number,
    _write_statement_header,
    _write_client_information,
    _write_statement_footer,
)

logger = get_application_logger('gdp_calculator')


def _configure_console_output():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    logger.info("Console configured for UTF-8 output")


def _prompt_gdp_value():
    """Prompt user for GDP value."""
    logger.info("Prompting for GDP value")
    while True:
        try:
            value = float(input("Enter the GDP value in TND (e.g., 44000000000 for 44 billion): "))
            if value <= 0:
                print("GDP value must be greater than 0. Please try again.")
                logger.warning("User entered invalid GDP value (<= 0)")
                continue
            logger.info(f"GDP value entered: {value:,.2f} TND")
            return value
        except ValueError:
            print("Invalid value. Please enter a number (example: 44000000000).")
            logger.warning("User entered invalid GDP value format")


def _prompt_start_year():
    """Prompt user for start year."""
    logger.info("Prompting for start year")
    while True:
        try:
            year = int(input("Enter the base year (2010-2026): "))
            if year < 2010 or year > 2026:
                print("Year must be between 2010 and 2026. Please try again.")
                logger.warning(f"User entered invalid start year: {year}")
                continue
            logger.info(f"Start year entered: {year}")
            return year
        except ValueError:
            print("Invalid year. Please enter a 4-digit year (example: 2020).")
            logger.warning("User entered invalid year format")


def _prompt_target_year():
    """Prompt user for target year."""
    logger.info("Prompting for target year")
    while True:
        try:
            year = int(input("Enter the target year (must be greater than base year): "))
            if year < 2011 or year > 2040:
                print("Year must be between 2011 and 2040. Please try again.")
                logger.warning(f"User entered invalid target year: {year}")
                continue
            logger.info(f"Target year entered: {year}")
            return year
        except ValueError:
            print("Invalid year. Please enter a 4-digit year (example: 2030).")
            logger.warning("User entered invalid year format")


def _prompt_scenario():
    """Prompt user for scenario selection."""
    logger.info("Prompting for scenario")
    print("\nSelect a growth scenario:")
    print("1. Optimistic (30% higher growth)")
    print("2. Baseline (historical average)")
    print("3. Pessimistic (30% lower growth)")
    
    while True:
        choice = input("Enter scenario number (1-3): ").strip()
        if choice == "1":
            logger.info("Scenario selected: optimistic")
            return "optimistic"
        elif choice == "2":
            logger.info("Scenario selected: baseline")
            return "baseline"
        elif choice == "3":
            logger.info("Scenario selected: pessimistic")
            return "pessimistic"
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            logger.warning(f"User entered invalid scenario choice: {choice}")


def _print_gdp_projection_table(projection: dict):
    """Print formatted GDP projection table."""
    print("\n" + "=" * 80)
    print("GDP PROJECTION ANALYSIS")
    print("=" * 80)
    
    print(f"\nInitial GDP: {projection['initial_gdp']:,.2f} TND")
    print(f"Base Year: {projection['start_year']}")
    print(f"Target Year: {projection['target_year']}")
    print(f"Scenario: {projection['scenario'].upper()}")
    print(f"Average Annual Growth: {projection['average_annual_growth']:.2f}%")
    
    print("\n" + "-" * 80)
    print("YEAR-BY-YEAR PROJECTION")
    print("-" * 80)
    print(f"{'Year':<10} {'GDP (TND)':<25} {'Annual Growth':<20} {'Cumulative Growth':<20}")
    print("-" * 80)
    
    prev_gdp = projection['initial_gdp']
    for year, gdp in projection['yearly_projections'].items():
        annual_growth = ((gdp - prev_gdp) / prev_gdp * 100) if prev_gdp != 0 else 0
        cumulative_growth = ((gdp - projection['initial_gdp']) / projection['initial_gdp'] * 100) if projection['initial_gdp'] != 0 else 0
        print(f"{year:<10} {gdp:>24,.2f} {annual_growth:>19.2f}% {cumulative_growth:>19.2f}%")
        prev_gdp = gdp
    
    print("-" * 80)
    print(f"\nProjected GDP ({projection['target_year']}): {projection['projected_gdp']:,.2f} TND")
    print(f"Total Growth: {projection['total_growth_percent']:.2f}%")
    print(f"Growth Multiplier: {projection['projected_gdp'] / projection['initial_gdp']:.2f}x")
    print("=" * 80)


def _write_gdp_projection_log(log_file_path: str, username: str, account_number: str, projection: dict):
    """Write GDP projection to log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%d/%m/%Y")
    
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        _write_statement_header(log_file, date_str)
        _write_client_information(log_file, username, account_number, timestamp)
        
        log_file.write("GDP PROJECTION ANALYSIS\n")
        log_file.write("-" * 76 + "\n")
        log_file.write(f"{'Initial GDP:':<20} {projection['initial_gdp']:>15,.2f} TND\n")
        log_file.write(f"{'Base Year:':<20} {projection['start_year']:>15}\n")
        log_file.write(f"{'Target Year:':<20} {projection['target_year']:>15}\n")
        log_file.write(f"{'Scenario:':<20} {projection['scenario'].upper():>15}\n")
        log_file.write(f"{'Average Annual Growth:':<20} {projection['average_annual_growth']:>14.2f}%\n\n")
        
        log_file.write("YEAR-BY-YEAR PROJECTION\n")
        log_file.write("-" * 76 + "\n")
        log_file.write(f"{'Year':<10} {'GDP (TND)':<25} {'Annual Growth':<20} {'Cumulative Growth':<20}\n")
        log_file.write("-" * 76 + "\n")
        
        prev_gdp = projection['initial_gdp']
        for year, gdp in projection['yearly_projections'].items():
            annual_growth = ((gdp - prev_gdp) / prev_gdp * 100) if prev_gdp != 0 else 0
            cumulative_growth = ((gdp - projection['initial_gdp']) / projection['initial_gdp'] * 100) if projection['initial_gdp'] != 0 else 0
            log_file.write(f"{year:<10} {gdp:>24,.2f} {annual_growth:>19.2f}% {cumulative_growth:>19.2f}%\n")
            prev_gdp = gdp
        
        log_file.write("-" * 76 + "\n")
        log_file.write(f"\nProjected GDP ({projection['target_year']}): {projection['projected_gdp']:,.2f} TND\n")
        log_file.write(f"Total Growth: {projection['total_growth_percent']:.2f}%\n")
        log_file.write(f"Growth Multiplier: {projection['projected_gdp'] / projection['initial_gdp']:.2f}x\n\n")
        
        log_file.write("NOTES\n")
        log_file.write("-" * 76 + "\n")
        log_file.write("- This projection is based on historical GDP growth rates from Tunisia\n")
        log_file.write("- Rates are approximate annual percentages from 2010 to 2026\n")
        log_file.write("- Scenarios apply modifiers to historical averages\n")
        log_file.write("- This document is for informational purposes only\n")
        log_file.write("- For official projections, please consult with economic institutions\n\n")
        
        _write_statement_footer(log_file)


def main():
    """Main function for GDP calculator."""
    logger.info("GDP calculator started")
    _configure_console_output()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        logger.info("Running in test mode")
        # Test with sample data
        projection = calculate_gdp_projection(
            initial_gdp=44000000000,
            start_year=2020,
            target_year=2035,
            scenario="baseline"
        )
        _print_gdp_projection_table(projection)
        return
    
    try:
        print("=== EcoPulse GDP Projection Calculator ===")
        print()
        
        username = get_username()
        account_number = get_account_number()
        logger.info(f"User: {username}, Account: {account_number or 'N/A'}")
        
        gdp_value = _prompt_gdp_value()
        start_year = _prompt_start_year()
        target_year = _prompt_target_year()
        scenario = _prompt_scenario()
        
        projection = calculate_gdp_projection(gdp_value, start_year, target_year, scenario)
        _print_gdp_projection_table(projection)
        
        # Generate log file
        safe_user = sanitize_filename(username)
        date_part = datetime.now().strftime("%Y%m%d")
        time_part = datetime.now().strftime("%H%M%S")
        log_file_path = f"gdp_projection_{safe_user}_{date_part}_{time_part}.log"
        
        _write_gdp_projection_log(log_file_path, username, account_number, projection)
        
        print(f"\nResults saved to: {log_file_path}")
        logger.info(f"GDP projection completed. Results saved to: {log_file_path}")
        
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
