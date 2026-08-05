#!/usr/bin/env python3
"""
Currency Converter
Converts between TND, USD, and EUR using historical exchange rates.
"""

import sys
import os
from datetime import datetime

# Add parent directory to path to import core modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.logger_config import get_application_logger
from core.tunisia_economic_indicators import (
    calculate_currency_conversion,
    EXCHANGE_RATES,
)
from core.tunisia_inflation_calculator import (
    sanitize_filename,
    get_username,
    get_account_number,
    _write_statement_header,
    _write_client_information,
    _write_statement_footer,
)

logger = get_application_logger('currency_converter')


def _configure_console_output():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    logger.info("Console configured for UTF-8 output")


def _prompt_amount():
    """Prompt user for amount to convert."""
    logger.info("Prompting for amount")
    while True:
        try:
            amount = float(input("Enter the amount to convert: "))
            if amount <= 0:
                print("Amount must be greater than 0. Please try again.")
                logger.warning("User entered invalid amount (<= 0)")
                continue
            logger.info(f"Amount entered: {amount}")
            return amount
        except ValueError:
            print("Invalid amount. Please enter a number (example: 1000).")
            logger.warning("User entered invalid amount format")


def _prompt_from_currency():
    """Prompt user for source currency."""
    logger.info("Prompting for source currency")
    print("\nAvailable currencies:")
    print("1. TND - Tunisian Dinar")
    print("2. USD - US Dollar")
    print("3. EUR - Euro")
    
    while True:
        choice = input("Select source currency (1-3): ").strip()
        if choice == "1":
            logger.info("Source currency selected: TND")
            return "TND"
        elif choice == "2":
            logger.info("Source currency selected: USD")
            return "USD"
        elif choice == "3":
            logger.info("Source currency selected: EUR")
            return "EUR"
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            logger.warning(f"User entered invalid currency choice: {choice}")


def _prompt_to_currency():
    """Prompt user for target currency."""
    logger.info("Prompting for target currency")
    print("\nAvailable currencies:")
    print("1. TND - Tunisian Dinar")
    print("2. USD - US Dollar")
    print("3. EUR - Euro")
    
    while True:
        choice = input("Select target currency (1-3): ").strip()
        if choice == "1":
            logger.info("Target currency selected: TND")
            return "TND"
        elif choice == "2":
            logger.info("Target currency selected: USD")
            return "USD"
        elif choice == "3":
            logger.info("Target currency selected: EUR")
            return "EUR"
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            logger.warning(f"User entered invalid currency choice: {choice}")


def _prompt_year():
    """Prompt user for year."""
    logger.info("Prompting for year")
    while True:
        try:
            year = int(input("Enter the year for exchange rate (2010-2026): "))
            if year < 2010 or year > 2026:
                print("Year must be between 2010 and 2026. Please try again.")
                logger.warning(f"User entered invalid year: {year}")
                continue
            logger.info(f"Year entered: {year}")
            return year
        except ValueError:
            print("Invalid year. Please enter a 4-digit year (example: 2020).")
            logger.warning("User entered invalid year format")


def _print_conversion_result(conversion: dict):
    """Print formatted conversion result."""
    print("\n" + "=" * 80)
    print("CURRENCY CONVERSION RESULT")
    print("=" * 80)
    
    print(f"\nAmount: {conversion['amount']:,.2f} {conversion['from_currency']}")
    print(f"Year: {conversion['year']}")
    print(f"Exchange Rate: {conversion['exchange_rate']:.4f}")
    print(f"\nConverted Amount: {conversion['converted_amount']:,.2f} {conversion['to_currency']}")
    
    # Show historical context
    print("\n" + "-" * 80)
    print("HISTORICAL EXCHANGE RATES")
    print("-" * 80)
    print(f"{'Year':<10} {'TND/USD':<15} {'TND/EUR':<15}")
    print("-" * 80)
    
    for year in sorted(EXCHANGE_RATES['USD'].keys()):
        if year >= 2010 and year <= 2026:
            usd_rate = EXCHANGE_RATES['USD'].get(year, 0)
            eur_rate = EXCHANGE_RATES['EUR'].get(year, 0)
            marker = " <--" if year == conversion['year'] else ""
            print(f"{year:<10} {usd_rate:<14.4f} {eur_rate:<14.4f}{marker}")
    
    print("=" * 80)


def _write_conversion_log(log_file_path: str, username: str, account_number: str, conversion: dict):
    """Write conversion to log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%d/%m/%Y")
    
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        _write_statement_header(log_file, date_str)
        _write_client_information(log_file, username, account_number, timestamp)
        
        log_file.write("CURRENCY CONVERSION\n")
        log_file.write("-" * 76 + "\n")
        log_file.write(f"{'Amount:':<20} {conversion['amount']:>15,.2f} {conversion['from_currency']}\n")
        log_file.write(f"{'From Currency:':<20} {conversion['from_currency']:>15}\n")
        log_file.write(f"{'To Currency:':<20} {conversion['to_currency']:>15}\n")
        log_file.write(f"{'Year:':<20} {conversion['year']:>15}\n")
        log_file.write(f"{'Exchange Rate:':<20} {conversion['exchange_rate']:>14.4f}\n")
        log_file.write(f"{'Converted Amount:':<20} {conversion['converted_amount']:>15,.2f} {conversion['to_currency']}\n\n")
        
        log_file.write("HISTORICAL CONTEXT\n")
        log_file.write("-" * 76 + "\n")
        log_file.write(f"{'Year':<10} {'TND/USD':<15} {'TND/EUR':<15}\n")
        log_file.write("-" * 76 + "\n")
        
        for year in sorted(EXCHANGE_RATES['USD'].keys()):
            if year >= 2010 and year <= 2026:
                usd_rate = EXCHANGE_RATES['USD'].get(year, 0)
                eur_rate = EXCHANGE_RATES['EUR'].get(year, 0)
                marker = " <--" if year == conversion['year'] else ""
                log_file.write(f"{year:<10} {usd_rate:<14.4f} {eur_rate:<14.4f}{marker}\n")
        
        log_file.write("\nNOTES\n")
        log_file.write("-" * 76 + "\n")
        log_file.write("- Exchange rates are annual averages from Central Bank of Tunisia\n")
        log_file.write("- Rates are approximate and may vary from daily rates\n")
        log_file.write("- This document is for informational purposes only\n")
        log_file.write("- For official transactions, please consult with financial institutions\n\n")
        
        _write_statement_footer(log_file)


def main():
    """Main function for currency converter."""
    logger.info("Currency converter started")
    _configure_console_output()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        logger.info("Running in test mode")
        # Test with sample data
        conversion = calculate_currency_conversion(
            amount=1000,
            from_currency="USD",
            to_currency="TND",
            year=2020
        )
        _print_conversion_result(conversion)
        return
    
    try:
        print("=== EcoPulse Currency Converter ===")
        print()
        
        username = get_username()
        account_number = get_account_number()
        logger.info(f"User: {username}, Account: {account_number or 'N/A'}")
        
        amount = _prompt_amount()
        from_currency = _prompt_from_currency()
        to_currency = _prompt_to_currency()
        year = _prompt_year()
        
        conversion = calculate_currency_conversion(amount, from_currency, to_currency, year)
        _print_conversion_result(conversion)
        
        # Generate log file
        safe_user = sanitize_filename(username)
        date_part = datetime.now().strftime("%Y%m%d")
        time_part = datetime.now().strftime("%H%M%S")
        log_file_path = f"currency_conversion_{safe_user}_{date_part}_{time_part}.log"
        
        _write_conversion_log(log_file_path, username, account_number, conversion)
        
        print(f"\nResults saved to: {log_file_path}")
        logger.info(f"Currency conversion completed. Results saved to: {log_file_path}")
        
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
