#!/usr/bin/env python3
"""
Tunisia Money Inflation Calculator
Calculates the value of money from 2010 to present day, using official inflation rates from Central Bank of Tunisia.
"""

import sys
from datetime import datetime
import re

from .logger_config import get_application_logger, setup_statement_logger

# Module logger
logger = get_application_logger('calculator')

# Tunisia inflation rates from 2010 to 2026 (official annual percentages)
INFLATION_RATES = {
    2010: 4.4,
    2011: 3.2,
    2012: 4.6,
    2013: 5.3,
    2014: 4.6,
    2015: 4.4,
    2016: 3.6,
    2017: 5.3,
    2018: 7.3,
    2019: 6.7,
    2020: 5.6,
    2021: 5.7,
    2022: 8.3,
    2023: 9.3,
    2024: 7.0,
    2025: 5.9,
    2026: 7.8  # Estimated for current year
}

def sanitize_filename(name: str) -> str:
    """Convert name to safe filename format."""
    cleaned = re.sub(r"\s+", "_", name.strip().lower())
    cleaned = re.sub(r"[^a-z0-9_\-]", "", cleaned)
    return cleaned or "user"

def get_username() -> str:
    """Get user's name for log file."""
    while True:
        name = input("Enter your name (used for your personal log file): ").strip()
        if name:
            return name
        print("Name cannot be empty. Please type your name and press Enter.")

def get_account_number() -> str:
    """Get optional account reference number."""
    return input("Enter an account/reference number (optional, press Enter to skip): ").strip()

def generate_log_filename(username: str) -> str:
    """Create unique log filename per user."""
    safe_name = sanitize_filename(username)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"log_{safe_name}_{timestamp}.log"

def _write_statement_header(log_file, date_str: str):
    log_file.write("\n" + "="*76 + "\n")
    log_file.write("="*76 + "\n")
    log_file.write("                 LAYAN SOCIETY FOR COST CALCULATION\n")
    log_file.write("                      AND RISK ESTIMATION\n")
    log_file.write("                      INFLATION ADJUSTMENT STATEMENT\n")
    log_file.write("="*76 + "\n")
    log_file.write(f"Date: {date_str:<65} Reference: TND/INF/2026/001\n")
    log_file.write("="*76 + "\n\n")

def _write_client_information(log_file, username: str, account_number: str, timestamp: str):
    log_file.write("CLIENT INFORMATION\n")
    log_file.write("-"*76 + "\n")
    log_file.write(f"{'Account Holder:':<20} {username}\n")
    log_file.write(f"{'Account Number:':<20} {account_number or 'N/A'}\n")
    log_file.write(f"{'Calculation Date:':<20} {timestamp}\n")
    log_file.write(f"{'Statement Type:':<20} Inflation Adjustment Analysis\n\n")

def _write_principal_amount_details(log_file, original_amount: float, start_year: int, adjusted_amount: float):
    log_file.write("PRINCIPAL AMOUNT DETAILS\n")
    log_file.write("-"*76 + "\n")
    log_file.write(f"{'Original Amount:':<20} {original_amount:>15,.2f} TND\n")
    log_file.write(f"{'Original Year:':<20} {start_year:>15}\n")
    log_file.write(f"{'Current Year:':<20} {'2026':>15}\n")
    log_file.write(f"{'Adjusted Amount:':<20} {adjusted_amount:>15,.2f} TND\n")

    inflation_amount = adjusted_amount - original_amount
    inflation_rate = ((adjusted_amount - original_amount) / original_amount) * 100
    log_file.write(f"{'Inflation Amount:':<20} {inflation_amount:>15,.2f} TND\n")
    log_file.write(f"{'Inflation Rate:':<20} {inflation_rate:>14.2f}%\n\n")

    return inflation_rate

def _write_additional_costs_breakdown(log_file, additional_costs):
    if additional_costs:
        log_file.write("ADDITIONAL COSTS BREAKDOWN\n")
        log_file.write("-"*76 + "\n")
        log_file.write(f"{'Cost #':<8} {'Original':<12} {'Year':<8} {'Adjusted':<15} {'Inflation':<12}\n")
        log_file.write("-"*76 + "\n")

        total_additional_original = 0
        total_additional_adjusted = 0

        for index, cost_item in enumerate(additional_costs, 1):
            original_cost = cost_item['amount']
            cost_year = cost_item['year']
            adjusted_cost = calculate_inflation(original_cost, cost_year)
            cost_inflation_rate = ((adjusted_cost - original_cost) / original_cost) * 100

            total_additional_original += original_cost
            total_additional_adjusted += adjusted_cost

            log_file.write(
                f"{index:<8} {original_cost:<12,.2f} {cost_year:<8} {adjusted_cost:<15,.2f} {cost_inflation_rate:<11.2f}%\n"
            )

        log_file.write("-"*76 + "\n")
        log_file.write(
            f"{'TOTALS:':<8} {total_additional_original:<12,.2f} {'':<8} {total_additional_adjusted:<15,.2f}\n\n"
        )
        return total_additional_adjusted

    log_file.write("ADDITIONAL COSTS BREAKDOWN\n")
    log_file.write("-"*76 + "\n")
    log_file.write("No additional costs declared.\n\n")
    return 0

def _write_financial_summary(log_file, adjusted_amount: float, total_additional_adjusted: float, grand_total: float, inflation_rate: float, original_amount: float):
    log_file.write("FINANCIAL SUMMARY\n")
    log_file.write("-"*76 + "\n")
    log_file.write(f"{'Principal Adjusted:':<25} {adjusted_amount:>20,.2f} TND\n")

    if total_additional_adjusted:
        log_file.write(f"{'Additional Costs Adj.:':<25} {total_additional_adjusted:>20,.2f} TND\n")

    log_file.write("-"*76 + "\n")
    log_file.write(f"{'TOTAL ADJUSTED AMOUNT:':<25} {grand_total:>20,.2f} TND\n")
    log_file.write(f"{'Purchasing Power Loss:':<25} {inflation_rate:>19.2f}%\n")
    log_file.write(f"{'Value Multiplier:':<25} {adjusted_amount/original_amount:>19.2f}x\n\n")

def _write_statement_footer(log_file):
    log_file.write("NOTES\n")
    log_file.write("-"*76 + "\n")
    log_file.write("- This calculation is based on official inflation rates from Tunisia\n")
    log_file.write("- Rates are approximate annual percentages from 2010 to 2026\n")
    log_file.write("- This document is for informational purposes only\n")
    log_file.write("- For official transactions, please consult with financial institutions\n\n")

    log_file.write("="*76 + "\n")
    log_file.write("                    AUTHORIZED SIGNATURE\n")
    log_file.write("                    ____________________\n")
    log_file.write("="*76 + "\n\n")

def log_calculation(log_file_path, username, account_number, original_amount, start_year, adjusted_amount, additional_costs, grand_total):
    """Log calculation results in bank statement format."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%d/%m/%Y")
    
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        _write_statement_header(log_file, date_str)
        _write_client_information(log_file, username, account_number, timestamp)
        inflation_rate = _write_principal_amount_details(log_file, original_amount, start_year, adjusted_amount)
        total_additional_adjusted = _write_additional_costs_breakdown(log_file, additional_costs)
        _write_financial_summary(
            log_file,
            adjusted_amount,
            total_additional_adjusted,
            grand_total,
            inflation_rate,
            original_amount,
        )
        _write_statement_footer(log_file)

def get_user_input():
    """Get user input for amount and additional costs."""
    logger.info("Getting user input for amount and year")
    while True:
        try:
            amount = float(input("Enter the main amount in Tunisian Dinars (TND), e.g. 1000: "))
            if amount <= 0:
                print("Amount must be greater than 0. Please try again.")
                logger.warning("User entered invalid amount (<= 0)")
                continue
            logger.info(f"Amount entered: {amount} TND")
            break
        except ValueError:
            print("Invalid amount. Please enter a number (example: 1000 or 1000.50).")
            logger.warning("User entered invalid amount format")
    
    while True:
        try:
            year = int(input("Enter the year of that amount (2010-2026): "))
            if year < 2010 or year > 2026:
                print("Year must be between 2010 and 2026. Please try again.")
                logger.warning(f"User entered invalid year: {year}")
                continue
            logger.info(f"Year entered: {year}")
            break
        except ValueError:
            print("Invalid year. Please enter a 4-digit year (example: 2020).")
            logger.warning("User entered invalid year format")
    
    additional_costs = []
    while True:
        add_costs = input("Do you want to add additional costs (y/n)? ").strip().lower()
        if add_costs in ("y", "n"):
            break
        print("Please type 'y' for yes or 'n' for no.")

    if add_costs == 'y':
        logger.info("User chose to add additional costs")
        print("\nEnter additional costs (enter 'done' when finished):")
        while True:
            cost_input = input("\nEnter cost amount in TND (or 'done' to finish): ").strip()
            if cost_input.lower() == 'done':
                break
            
            try:
                cost_amount = float(cost_input)
                if cost_amount < 0:
                    print("Cost amount cannot be negative.")
                    logger.warning("User entered negative cost amount")
                    continue
            except ValueError:
                print("Invalid cost amount. Please enter a number (example: 150 or 150.75).")
                logger.warning("User entered invalid cost amount format")
                continue
            
            while True:
                try:
                    cost_year = int(input(f"Enter the year for this cost ({cost_amount} TND) (2010-2026): "))
                    if cost_year < 2010 or cost_year > 2026:
                        print("Please enter a year between 2010 and 2026.")
                        logger.warning(f"User entered invalid cost year: {cost_year}")
                        continue
                    break
                except ValueError:
                    print("Invalid year. Please enter a 4-digit year (example: 2023).")
                    logger.warning("User entered invalid cost year format")
            
            additional_costs.append({'amount': cost_amount, 'year': cost_year})
            print(f"Added: {cost_amount} TND from {cost_year}")
            logger.info(f"Additional cost added: {cost_amount} TND from {cost_year}")
    else:
        logger.info("User chose not to add additional costs")
    
    return amount, year, additional_costs

def calculate_inflation(amount, start_year, end_year=2026):
    """Calculate the inflation-adjusted amount from start_year to end_year."""
    logger.debug(f"Calculating inflation: {amount} TND from {start_year} to {end_year}")
    if start_year == end_year:
        logger.debug("Start year equals end year, returning original amount")
        return amount
    
    adjusted_amount = amount

    for year in range(start_year + 1, end_year + 1):
        if year in INFLATION_RATES:
            inflation_rate = INFLATION_RATES[year] / 100
            adjusted_amount *= (1 + inflation_rate)
    
    logger.debug(f"Inflation calculation result: {adjusted_amount:.2f} TND")
    return adjusted_amount

def _total_adjusted_additional_costs(additional_costs):
    return sum(calculate_inflation(cost['amount'], cost['year']) for cost in additional_costs)

def display_results(original_amount, start_year, adjusted_amount, additional_costs, grand_total):
    """Display the calculation results."""
    logger.info("Displaying calculation results")
    print("\n" + "="*60)
    print("CALCULATION RESULTS")
    print("="*60)
    print(f"Original Amount (TND): {original_amount:,.2f}")
    print(f"Original Year: {start_year}")
    print(f"Inflation-Adjusted Amount (2026): {adjusted_amount:,.2f}")
    
    # Calculate and display additional costs with inflation adjustment
    total_additional_costs = 0
    if additional_costs:
        print(f"\nAdditional Costs (inflation-adjusted to 2026):")
        print("-" * 50)
        for i, cost in enumerate(additional_costs, 1):
            original_cost = cost['amount']
            cost_year = cost['year']
            adjusted_cost = calculate_inflation(original_cost, cost_year)
            total_additional_costs += adjusted_cost
            print(f"  Cost {i}: {original_cost:,.2f} TND from {cost_year} -> {adjusted_cost:,.2f} TND (2026)")
        
        print(f"\nTotal Additional Costs (2026): {total_additional_costs:,.2f}")
    else:
        print(f"\nAdditional Costs: 0.00")
    
    # Calculate total with adjusted costs
    grand_total = adjusted_amount + total_additional_costs
    print(f"\nGrand Total (2026): {grand_total:,.2f}")
    
    # Calculate purchasing power loss
    purchasing_power_loss = ((adjusted_amount - original_amount) / original_amount) * 100
    print(f"\nPurchasing Power Loss (main amount): {purchasing_power_loss:.1f}%")
    print(f"Value Multiplier (main amount): {adjusted_amount/original_amount:.2f}x")
    
    # Show year-by-year breakdown
    print("\n" + "-"*40)
    print("YEAR-BY-YEAR BREAKDOWN (MAIN AMOUNT)")
    print("-"*40)
    
    current_amount = original_amount
    print(f"{start_year}: {current_amount:,.2f} TND")
    
    for year in range(start_year + 1, 2027):
        if year - 1 in INFLATION_RATES:
            inflation_rate = INFLATION_RATES[year - 1]
            current_amount *= (1 + inflation_rate / 100)
            print(f"{year}: {current_amount:,.2f} TND (inflation: {inflation_rate}%)")

def test_calculator():
    """Test the calculator with sample data."""
    logger.info("Running calculator tests")
    print("=== RUNNING TESTS ===")
    print()
    
    # Test case 1: 1000 TND from 2010
    print("Test 1: 1000 TND from 2010")
    amount = 1000
    year = 2010
    additional_costs = []
    
    adjusted_amount = calculate_inflation(amount, year)
    total_additional_costs = 0
    for cost in additional_costs:
        adjusted_cost = calculate_inflation(cost['amount'], cost['year'])
        total_additional_costs += adjusted_cost
    grand_total = adjusted_amount + total_additional_costs
    
    print(f"Original: {amount} TND in {year}")
    print(f"Adjusted (2024): {adjusted_amount:.2f} TND")
    print(f"Multiplier: {adjusted_amount/amount:.2f}x")
    print()
    
    # Test case 2: 500 TND from 2015 with multiple additional costs from different years
    print("Test 2: 500 TND from 2015 with multiple additional costs")
    amount = 500
    year = 2015
    additional_costs = [
        {'amount': 50, 'year': 2018},
        {'amount': 30, 'year': 2020},
        {'amount': 20, 'year': 2022}
    ]
    
    adjusted_amount = calculate_inflation(amount, year)
    total_additional_costs = 0
    print("Additional costs breakdown:")
    for cost in additional_costs:
        adjusted_cost = calculate_inflation(cost['amount'], cost['year'])
        total_additional_costs += adjusted_cost
        print(f"  {cost['amount']} TND from {cost['year']} -> {adjusted_cost:.2f} TND (2024)")
    
    grand_total = adjusted_amount + total_additional_costs
    
    print(f"\nOriginal amount: {amount} TND in {year}")
    print(f"Adjusted (2024): {adjusted_amount:.2f} TND")
    print(f"Total additional costs (2024): {total_additional_costs:.2f} TND")
    print(f"Grand total: {grand_total:.2f} TND")
    print()
    
    # Test case 3: 100 TND from 2020 with one additional cost
    print("Test 3: 100 TND from 2020 with one additional cost")
    amount = 100
    year = 2020
    additional_costs = [{'amount': 25, 'year': 2021}]
    
    adjusted_amount = calculate_inflation(amount, year)
    total_additional_costs = 0
    for cost in additional_costs:
        adjusted_cost = calculate_inflation(cost['amount'], cost['year'])
        total_additional_costs += adjusted_cost
        print(f"Additional cost: {cost['amount']} TND from {cost['year']} -> {adjusted_cost:.2f} TND (2024)")
    
    grand_total = adjusted_amount + total_additional_costs
    
    print(f"Original: {amount} TND in {year}")
    print(f"Adjusted (2024): {adjusted_amount:.2f} TND")
    print(f"Grand total: {grand_total:.2f} TND")
    print()
    
    print("=== TESTS COMPLETED ===")
    print()

def main():
    """Main function to run the inflation calculator."""
    logger.info("Inflation calculator started")
    # Check if running in test mode
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_calculator()
        return
    
    try:
        print("=== Tunisia Money Inflation Calculator (2010-2026) ===")
        print()
        
        # Capture user identity early (used for unique per-user logging)
        username = get_username()
        account_number = get_account_number()
        logger.info(f"User: {username}, Account: {account_number or 'N/A'}")

        # Generate unique log file name per user
        log_file_path = generate_log_filename(username)
        print(f"Your statement will be saved to: {log_file_path}")
        logger.info(f"Statement log file: {log_file_path}")
        print()
        
        # Get user input
        amount, year, additional_costs = get_user_input()
        
        # Calculate inflation-adjusted amount
        adjusted_amount = calculate_inflation(amount, year)
        
        # Calculate total with additional costs
        total_additional_costs = _total_adjusted_additional_costs(additional_costs)
        
        grand_total = adjusted_amount + total_additional_costs
        
        # Display results
        display_results(amount, year, adjusted_amount, additional_costs, grand_total)
        
        # Log results to file
        log_calculation(log_file_path, username, account_number, amount, year, adjusted_amount, additional_costs, grand_total)
        
        print(f"\nResults saved to: {log_file_path}")
        logger.info(f"Calculation completed successfully. Results saved to: {log_file_path}")
        print("\n" + "="*60)
        print("Calculation completed successfully!")
        print("="*60)
        
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
