#!/usr/bin/env python3
"""
Interest Impact Calculator
Calculates the impact of interest rates on investments and loans.
"""

import sys
import os
from datetime import datetime

# Add parent directory to path to import core modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.logger_config import get_application_logger
from core.tunisia_economic_indicators import (
    calculate_interest_impact,
    CENTRAL_BANK_RATES,
)
from core.tunisia_inflation_calculator import (
    sanitize_filename,
    get_username,
    get_account_number,
    _write_statement_header,
    _write_client_information,
    _write_statement_footer,
)

logger = get_application_logger('interest_calculator')


def _configure_console_output():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    logger.info("Console configured for UTF-8 output")


def _prompt_principal():
    """Prompt user for principal amount."""
    logger.info("Prompting for principal amount")
    while True:
        try:
            principal = float(input("Enter the principal amount in TND: "))
            if principal <= 0:
                print("Principal must be greater than 0. Please try again.")
                logger.warning("User entered invalid principal (<= 0)")
                continue
            logger.info(f"Principal entered: {principal:,.2f} TND")
            return principal
        except ValueError:
            print("Invalid amount. Please enter a number (example: 10000).")
            logger.warning("User entered invalid principal format")


def _prompt_years():
    """Prompt user for number of years."""
    logger.info("Prompting for years")
    while True:
        try:
            years = int(input("Enter the number of years: "))
            if years <= 0:
                print("Years must be greater than 0. Please try again.")
                logger.warning("User entered invalid years (<= 0)")
                continue
            logger.info(f"Years entered: {years}")
            return years
        except ValueError:
            print("Invalid number. Please enter a positive integer (example: 5).")
            logger.warning("User entered invalid years format")


def _prompt_start_year():
    """Prompt user for start year."""
    logger.info("Prompting for start year")
    while True:
        try:
            year = int(input("Enter the start year (2010-2026): "))
            if year < 2010 or year > 2026:
                print("Year must be between 2010 and 2026. Please try again.")
                logger.warning(f"User entered invalid start year: {year}")
                continue
            logger.info(f"Start year entered: {year}")
            return year
        except ValueError:
            print("Invalid year. Please enter a 4-digit year (example: 2020).")
            logger.warning("User entered invalid year format")


def _prompt_scenario():
    """Prompt user for scenario selection."""
    logger.info("Prompting for scenario")
    print("\nSelect an interest rate scenario:")
    print("1. Optimistic (lower interest rates - good for borrowers)")
    print("2. Baseline (historical average)")
    print("3. Pessimistic (higher interest rates - bad for borrowers)")
    
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


def _print_interest_impact_table(impact: dict):
    """Print formatted interest impact table."""
    print("\n" + "=" * 80)
    print("INTEREST RATE IMPACT ANALYSIS")
    print("=" * 80)
    
    print(f"\nPrincipal: {impact['principal']:,.2f} TND")
    print(f"Duration: {impact['years']} years")
    print(f"Start Year: {impact['start_year']}")
    print(f"Scenario: {impact['scenario'].upper()}")
    print(f"Average Annual Rate: {impact['average_rate']:.2f}%")
    
    print("\n" + "-" * 80)
    print("YEAR-BY-YEAR BREAKDOWN")
    print("-" * 80)
    print(f"{'Year':<10} {'Balance':<25} {'Annual Interest':<25} {'Total Interest':<20}")
    print("-" * 80)
    
    prev_balance = impact['principal']
    for year, balance in impact['yearly_breakdown'].items():
        annual_interest = balance - prev_balance
        total_interest = balance - impact['principal']
        print(f"{year:<10} {balance:>23,.2f} {annual_interest:>23,.2f} {total_interest:>19,.2f}")
        prev_balance = balance
    
    print("-" * 80)
    print(f"\nFinal Amount: {impact['final_amount']:,.2f} TND")
    print(f"Total Interest: {impact['total_interest']:,.2f} TND")
    print(f"Interest Percentage: {impact['interest_percentage']:.2f}%")
    print(f"Multiplier: {impact['final_amount'] / impact['principal']:.2f}x")
    
    # Interpret the result
    if impact['interest_percentage'] > 50:
        print("Interpretation: High interest accumulation - significant growth")
    elif impact['interest_percentage'] > 20:
        print("Interpretation: Moderate interest accumulation")
    else:
        print("Interpretation: Low interest accumulation")
    
    print("=" * 80)


def _write_interest_impact_log(log_file_path: str, username: str, account_number: str, impact: dict):
    """Write interest impact to log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%d/%m/%Y")
    
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        _write_statement_header(log_file, date_str)
        _write_client_information(log_file, username, account_number, timestamp)
        
        log_file.write("INTEREST RATE IMPACT ANALYSIS\n")
        log_file.write("-" * 76 + "\n")
        log_file.write(f"{'Principal:':<20} {impact['principal']:>15,.2f} TND\n")
        log_file.write(f"{'Duration:':<20} {impact['years']:>15} years\n")
        log_file.write(f"{'Start Year:':<20} {impact['start_year']:>15}\n")
        log_file.write(f"{'Scenario:':<20} {impact['scenario'].upper():>15}\n")
        log_file.write(f"{'Average Rate:':<20} {impact['average_rate']:>14.2f}%\n\n")
        
        log_file.write("YEAR-BY-YEAR BREAKDOWN\n")
        log_file.write("-" * 76 + "\n")
        log_file.write(f"{'Year':<10} {'Balance':<25} {'Annual Interest':<25} {'Total Interest':<20}\n")
        log_file.write("-" * 76 + "\n")
        
        prev_balance = impact['principal']
        for year, balance in impact['yearly_breakdown'].items():
            annual_interest = balance - prev_balance
            total_interest = balance - impact['principal']
            log_file.write(f"{year:<10} {balance:>23,.2f} {annual_interest:>23,.2f} {total_interest:>19,.2f}\n")
            prev_balance = balance
        
        log_file.write("-" * 76 + "\n")
        log_file.write(f"\nFinal Amount: {impact['final_amount']:,.2f} TND\n")
        log_file.write(f"Total Interest: {impact['total_interest']:,.2f} TND\n")
        log_file.write(f"Interest Percentage: {impact['interest_percentage']:.2f}%\n")
        log_file.write(f"Multiplier: {impact['final_amount'] / impact['principal']:.2f}x\n\n")
        
        # Interpretation
        if impact['interest_percentage'] > 50:
            interpretation = "High interest accumulation - significant growth"
        elif impact['interest_percentage'] > 20:
            interpretation = "Moderate interest accumulation"
        else:
            interpretation = "Low interest accumulation"
        
        log_file.write(f"Interpretation: {interpretation}\n\n")
        
        log_file.write("NOTES\n")
        log_file.write("-" * 76 + "\n")
        log_file.write("- This calculation is based on Central Bank of Tunisia interest rates\n")
        log_file.write("- Rates are approximate annual percentages from 2010 to 2026\n")
        log_file.write("- Scenarios apply modifiers to historical averages\n")
        log_file.write("- Compound interest is calculated annually\n")
        log_file.write("- This document is for informational purposes only\n")
        log_file.write("- For official calculations, please consult with financial institutions\n\n")
        
        _write_statement_footer(log_file)


def main():
    """Main function for interest calculator."""
    logger.info("Interest calculator started")
    _configure_console_output()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        logger.info("Running in test mode")
        # Test with sample data
        impact = calculate_interest_impact(
            principal=10000,
            years=5,
            start_year=2020,
            scenario="baseline"
        )
        _print_interest_impact_table(impact)
        return
    
    try:
        print("=== EcoPulse Interest Rate Impact Calculator ===")
        print()
        
        username = get_username()
        account_number = get_account_number()
        logger.info(f"User: {username}, Account: {account_number or 'N/A'}")
        
        principal = _prompt_principal()
        years = _prompt_years()
        start_year = _prompt_start_year()
        scenario = _prompt_scenario()
        
        impact = calculate_interest_impact(principal, years, start_year, scenario)
        _print_interest_impact_table(impact)
        
        # Generate log file
        safe_user = sanitize_filename(username)
        date_part = datetime.now().strftime("%Y%m%d")
        time_part = datetime.now().strftime("%H%M%S")
        log_file_path = f"interest_impact_{safe_user}_{date_part}_{time_part}.log"
        
        _write_interest_impact_log(log_file_path, username, account_number, impact)
        
        print(f"\nResults saved to: {log_file_path}")
        logger.info(f"Interest impact calculation completed. Results saved to: {log_file_path}")
        
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
