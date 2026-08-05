#!/usr/bin/env python3
"""
Unemployment Impact Calculator
Projects unemployment rates and analyzes economic impact.
"""

import sys
import os
from datetime import datetime

# Add parent directory to path to import core modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.logger_config import get_application_logger
from core.tunisia_economic_indicators import (
    calculate_unemployment_impact,
    get_economic_summary,
    UNEMPLOYMENT_RATES,
)
from core.tunisia_inflation_calculator import (
    sanitize_filename,
    get_username,
    get_account_number,
    _write_statement_header,
    _write_client_information,
    _write_statement_footer,
)

logger = get_application_logger('unemployment_calculator')


def _configure_console_output():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    logger.info("Console configured for UTF-8 output")


def _prompt_unemployment_rate():
    """Prompt user for unemployment rate."""
    logger.info("Prompting for unemployment rate")
    while True:
        try:
            rate = float(input("Enter the current unemployment rate (percentage, e.g., 15.5): "))
            if rate <= 0 or rate > 100:
                print("Unemployment rate must be between 0 and 100. Please try again.")
                logger.warning("User entered invalid unemployment rate")
                continue
            logger.info(f"Unemployment rate entered: {rate}%")
            return rate
        except ValueError:
            print("Invalid rate. Please enter a number (example: 15.5).")
            logger.warning("User entered invalid unemployment rate format")


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
    print("\nSelect a labor market scenario:")
    print("1. Optimistic (faster improvement)")
    print("2. Baseline (historical trend)")
    print("3. Pessimistic (slower improvement or worsening)")
    
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


def _print_unemployment_projection_table(projection: dict):
    """Print formatted unemployment projection table."""
    print("\n" + "=" * 80)
    print("UNEMPLOYMENT RATE PROJECTION")
    print("=" * 80)
    
    print(f"\nInitial Unemployment Rate: {projection['initial_rate']:.2f}%")
    print(f"Base Year: {projection['start_year']}")
    print(f"Target Year: {projection['target_year']}")
    print(f"Scenario: {projection['scenario'].upper()}")
    print(f"Annual Change: {projection['annual_change']:.3f}%")
    
    print("\n" + "-" * 80)
    print("YEAR-BY-YEAR PROJECTION")
    print("-" * 80)
    print(f"{'Year':<10} {'Unemployment Rate':<20} {'Annual Change':<20} {'Total Change':<20}")
    print("-" * 80)
    
    for year, rate in projection['yearly_projections'].items():
        annual_change = projection['annual_change']
        total_change = rate - projection['initial_rate']
        print(f"{year:<10} {rate:>18.2f}% {annual_change:>19.3f}% {total_change:>19.2f}%")
    
    print("-" * 80)
    print(f"\nProjected Unemployment ({projection['target_year']}): {projection['projected_rate']:.2f}%")
    print(f"Total Change: {projection['total_change']:+.2f}%")
    
    # Interpret the result
    if projection['total_change'] < -2:
        print("Interpretation: Significant improvement in labor market")
    elif projection['total_change'] < 0:
        print("Interpretation: Moderate improvement in labor market")
    elif projection['total_change'] < 2:
        print("Interpretation: Stable labor market conditions")
    else:
        print("Interpretation: Labor market deterioration")
    
    print("=" * 80)


def _write_unemployment_projection_log(log_file_path: str, username: str, account_number: str, projection: dict):
    """Write unemployment projection to log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%d/%m/%Y")
    
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        _write_statement_header(log_file, date_str)
        _write_client_information(log_file, username, account_number, timestamp)
        
        log_file.write("UNEMPLOYMENT RATE PROJECTION\n")
        log_file.write("-" * 76 + "\n")
        log_file.write(f"{'Initial Rate:':<20} {projection['initial_rate']:>15.2f}%\n")
        log_file.write(f"{'Base Year:':<20} {projection['start_year']:>15}\n")
        log_file.write(f"{'Target Year:':<20} {projection['target_year']:>15}\n")
        log_file.write(f"{'Scenario:':<20} {projection['scenario'].upper():>15}\n")
        log_file.write(f"{'Annual Change:':<20} {projection['annual_change']:>14.3f}%\n\n")
        
        log_file.write("YEAR-BY-YEAR PROJECTION\n")
        log_file.write("-" * 76 + "\n")
        log_file.write(f"{'Year':<10} {'Unemployment Rate':<20} {'Annual Change':<20} {'Total Change':<20}\n")
        log_file.write("-" * 76 + "\n")
        
        for year, rate in projection['yearly_projections'].items():
            annual_change = projection['annual_change']
            total_change = rate - projection['initial_rate']
            log_file.write(f"{year:<10} {rate:>18.2f}% {annual_change:>19.3f}% {total_change:>19.2f}%\n")
        
        log_file.write("-" * 76 + "\n")
        log_file.write(f"\nProjected Unemployment ({projection['target_year']}): {projection['projected_rate']:.2f}%\n")
        log_file.write(f"Total Change: {projection['total_change']:+.2f}%\n\n")
        
        # Interpretation
        if projection['total_change'] < -2:
            interpretation = "Significant improvement in labor market"
        elif projection['total_change'] < 0:
            interpretation = "Moderate improvement in labor market"
        elif projection['total_change'] < 2:
            interpretation = "Stable labor market conditions"
        else:
            interpretation = "Labor market deterioration"
        
        log_file.write(f"Interpretation: {interpretation}\n\n")
        
        log_file.write("NOTES\n")
        log_file.write("-" * 76 + "\n")
        log_file.write("- This projection is based on historical unemployment rates from Tunisia\n")
        log_file.write("- Rates are approximate annual percentages from 2010 to 2026\n")
        log_file.write("- Scenarios apply modifiers to historical trends\n")
        log_file.write("- This document is for informational purposes only\n")
        log_file.write("- For official projections, please consult with economic institutions\n\n")
        
        _write_statement_footer(log_file)


def main():
    """Main function for unemployment calculator."""
    logger.info("Unemployment calculator started")
    _configure_console_output()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        logger.info("Running in test mode")
        # Test with sample data
        projection = calculate_unemployment_impact(
            initial_rate=15.5,
            start_year=2020,
            target_year=2035,
            scenario="baseline"
        )
        _print_unemployment_projection_table(projection)
        return
    
    try:
        print("=== EcoPulse Unemployment Rate Projection Calculator ===")
        print()
        
        username = get_username()
        account_number = get_account_number()
        logger.info(f"User: {username}, Account: {account_number or 'N/A'}")
        
        unemployment_rate = _prompt_unemployment_rate()
        start_year = _prompt_start_year()
        target_year = _prompt_target_year()
        scenario = _prompt_scenario()
        
        projection = calculate_unemployment_impact(unemployment_rate, start_year, target_year, scenario)
        _print_unemployment_projection_table(projection)
        
        # Generate log file
        safe_user = sanitize_filename(username)
        date_part = datetime.now().strftime("%Y%m%d")
        time_part = datetime.now().strftime("%H%M%S")
        log_file_path = f"unemployment_projection_{safe_user}_{date_part}_{time_part}.log"
        
        _write_unemployment_projection_log(log_file_path, username, account_number, projection)
        
        print(f"\nResults saved to: {log_file_path}")
        logger.info(f"Unemployment projection completed. Results saved to: {log_file_path}")
        
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
