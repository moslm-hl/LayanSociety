#!/usr/bin/env python3
"""
Tunisia Economic Indicators Module
Comprehensive economic data for Tunisia including GDP, unemployment, interest rates, and exchange rates.
"""

from logger_config import get_application_logger

logger = get_application_logger('economic_indicators')

# Tunisia GDP Growth Rates (annual percentage)
# Source: World Bank, IMF, National Statistics Institute
GDP_GROWTH_RATES = {
    2010: 3.7,
    2011: -1.1,  # Arab Spring impact
    2012: 3.6,
    2013: 2.4,
    2014: 2.3,
    2015: 0.9,
    2016: 1.0,
    2017: 1.8,
    2018: 2.7,
    2019: 1.1,
    2020: -8.8,  # COVID-19 impact
    2021: 4.3,
    2022: 2.4,
    2023: 0.8,
    2024: 1.3,
    2025: 1.8,  # Projected
    2026: 2.2,  # Projected
}

# Tunisia Unemployment Rates (annual percentage)
UNEMPLOYMENT_RATES = {
    2010: 13.0,
    2011: 18.9,  # Post-revolution spike
    2012: 16.7,
    2013: 15.7,
    2014: 15.2,
    2015: 15.3,
    2016: 15.5,
    2017: 15.2,
    2018: 15.5,
    2019: 15.0,
    2020: 16.2,  # COVID-19 impact
    2021: 17.8,
    2022: 16.2,
    2023: 16.1,
    2024: 15.5,
    2025: 15.0,  # Projected
    2026: 14.5,  # Projected
}

# Tunisia Central Bank Interest Rates (annual percentage)
CENTRAL_BANK_RATES = {
    2010: 4.25,
    2011: 3.75,
    2012: 3.75,
    2013: 3.75,
    2014: 3.75,
    2015: 4.00,
    2016: 4.25,
    2017: 4.75,
    2018: 5.75,
    2019: 7.75,
    2020: 6.75,
    2021: 6.75,
    2022: 7.75,
    2023: 8.00,
    2024: 7.50,
    2025: 7.00,  # Projected
    2026: 6.50,  # Projected
}

# Tunisia Currency Exchange Rates (TND per foreign currency)
# Average annual rates
EXCHANGE_RATES = {
    'USD': {
        2010: 1.42,
        2011: 1.42,
        2012: 1.52,
        2013: 1.62,
        2014: 1.68,
        2015: 1.82,
        2016: 2.05,
        2017: 2.30,
        2018: 2.48,
        2019: 2.85,
        2020: 2.85,
        2021: 2.78,
        2022: 3.12,
        2023: 3.10,
        2024: 3.08,
        2025: 3.05,  # Projected
        2026: 3.02,  # Projected
    },
    'EUR': {
        2010: 1.88,
        2011: 1.98,
        2012: 1.95,
        2013: 2.12,
        2014: 2.21,
        2015: 2.23,
        2016: 2.26,
        2017: 2.54,
        2018: 2.86,
        2019: 3.18,
        2020: 3.12,
        2021: 3.35,
        2022: 3.30,
        2023: 3.36,
        2024: 3.34,
        2025: 3.31,  # Projected
        2026: 3.28,  # Projected
    },
}

# Tunisia GDP in current US Dollars (billions)
GDP_VALUES = {
    2010: 44.0,
    2011: 46.0,
    2012: 46.5,
    2013: 47.0,
    2014: 47.5,
    2015: 43.0,
    2016: 42.0,
    2017: 40.0,
    2018: 40.5,
    2019: 41.0,
    2020: 37.0,
    2021: 44.0,
    2022: 46.0,
    2023: 47.0,
    2024: 48.0,
    2025: 49.5,  # Projected
    2026: 51.0,  # Projected
}


def calculate_gdp_projection(initial_gdp: float, start_year: int, target_year: int, scenario: str = "baseline") -> dict:
    """
    Calculate GDP projection based on historical growth rates.
    
    Args:
        initial_gdp: Initial GDP value in TND or USD
        start_year: Starting year for projection
        target_year: Target year for projection
        scenario: "optimistic", "baseline", or "pessimistic"
    
    Returns:
        Dictionary with projection details
    """
    logger.info(f"Calculating GDP projection: {initial_gdp} from {start_year} to {target_year}, scenario: {scenario}")
    
    if start_year < 2010 or start_year > 2026:
        raise ValueError("start_year must be between 2010 and 2026")
    
    if target_year <= start_year:
        raise ValueError("target_year must be greater than start_year")
    
    # Calculate average growth rate from historical data
    years = list(range(start_year, 2027))
    growth_rates = [GDP_GROWTH_RATES.get(year, 0) for year in years]
    avg_growth = sum(growth_rates) / len(growth_rates)
    
    # Apply scenario modifiers
    scenario_modifiers = {
        "optimistic": 1.3,  # 30% higher growth
        "baseline": 1.0,
        "pessimistic": 0.7,  # 30% lower growth
    }
    
    modifier = scenario_modifiers.get(scenario, 1.0)
    adjusted_growth = avg_growth * modifier / 100
    
    # Project GDP year by year
    projected_gdp = initial_gdp
    yearly_projections = {start_year: initial_gdp}
    
    for year in range(start_year + 1, target_year + 1):
        projected_gdp *= (1 + adjusted_growth)
        yearly_projections[year] = projected_gdp
    
    total_growth = ((projected_gdp - initial_gdp) / initial_gdp) * 100
    
    result = {
        "initial_gdp": initial_gdp,
        "start_year": start_year,
        "target_year": target_year,
        "scenario": scenario,
        "projected_gdp": projected_gdp,
        "total_growth_percent": total_growth,
        "average_annual_growth": avg_growth * modifier,
        "yearly_projections": yearly_projections,
    }
    
    logger.info(f"GDP projection result: {projected_gdp:.2f} ({total_growth:.2f}% growth)")
    return result


def calculate_unemployment_impact(initial_rate: float, start_year: int, target_year: int, scenario: str = "baseline") -> dict:
    """
    Calculate unemployment rate projection.
    
    Args:
        initial_rate: Initial unemployment rate (percentage)
        start_year: Starting year
        target_year: Target year
        scenario: "optimistic", "baseline", or "pessimistic"
    
    Returns:
        Dictionary with unemployment projection details
    """
    logger.info(f"Calculating unemployment projection: {initial_rate}% from {start_year} to {target_year}, scenario: {scenario}")
    
    if start_year < 2010 or start_year > 2026:
        raise ValueError("start_year must be between 2010 and 2026")
    
    if target_year <= start_year:
        raise ValueError("target_year must be greater than start_year")
    
    # Calculate average unemployment trend
    years = list(range(start_year, 2027))
    unemployment_rates = [UNEMPLOYMENT_RATES.get(year, 15.0) for year in years]
    avg_unemployment = sum(unemployment_rates) / len(unemployment_rates)
    
    # Calculate trend (improving or worsening)
    trend = (unemployment_rates[-1] - unemployment_rates[0]) / len(unemployment_rates)
    
    # Apply scenario modifiers
    scenario_modifiers = {
        "optimistic": 1.5,  # Faster improvement
        "baseline": 1.0,
        "pessimistic": 0.5,  # Slower improvement or worsening
    }
    
    modifier = scenario_modifiers.get(scenario, 1.0)
    annual_change = trend * modifier
    
    # Project unemployment year by year
    projected_rate = initial_rate
    yearly_projections = {start_year: initial_rate}
    
    for year in range(start_year + 1, target_year + 1):
        projected_rate += annual_change
        # Keep within reasonable bounds
        projected_rate = max(5.0, min(30.0, projected_rate))
        yearly_projections[year] = projected_rate
    
    total_change = projected_rate - initial_rate
    
    result = {
        "initial_rate": initial_rate,
        "start_year": start_year,
        "target_year": target_year,
        "scenario": scenario,
        "projected_rate": projected_rate,
        "total_change": total_change,
        "annual_change": annual_change,
        "yearly_projections": yearly_projections,
    }
    
    logger.info(f"Unemployment projection result: {projected_rate:.2f}% ({total_change:+.2f}% change)")
    return result


def calculate_currency_conversion(amount: float, from_currency: str, to_currency: str, year: int) -> dict:
    """
    Convert currency based on historical exchange rates.
    
    Args:
        amount: Amount to convert
        from_currency: Source currency (TND, USD, EUR)
        to_currency: Target currency (TND, USD, EUR)
        year: Year for exchange rate
    
    Returns:
        Dictionary with conversion details
    """
    logger.info(f"Converting {amount} {from_currency} to {to_currency} for year {year}")
    
    currencies = ['TND', 'USD', 'EUR']
    
    if from_currency not in currencies or to_currency not in currencies:
        raise ValueError(f"Currencies must be one of: {currencies}")
    
    if year < 2010 or year > 2026:
        raise ValueError("year must be between 2010 and 2026")
    
    # Get exchange rates for the year
    if from_currency == 'TND' and to_currency == 'USD':
        rate = 1.0 / EXCHANGE_RATES['USD'].get(year, 2.85)
        converted = amount * rate
    elif from_currency == 'TND' and to_currency == 'EUR':
        rate = 1.0 / EXCHANGE_RATES['EUR'].get(year, 3.12)
        converted = amount * rate
    elif from_currency == 'USD' and to_currency == 'TND':
        rate = EXCHANGE_RATES['USD'].get(year, 2.85)
        converted = amount * rate
    elif from_currency == 'USD' and to_currency == 'EUR':
        tnd_amount = amount * EXCHANGE_RATES['USD'].get(year, 2.85)
        converted = tnd_amount / EXCHANGE_RATES['EUR'].get(year, 3.12)
    elif from_currency == 'EUR' and to_currency == 'TND':
        rate = EXCHANGE_RATES['EUR'].get(year, 3.12)
        converted = amount * rate
    elif from_currency == 'EUR' and to_currency == 'USD':
        tnd_amount = amount * EXCHANGE_RATES['EUR'].get(year, 3.12)
        converted = tnd_amount / EXCHANGE_RATES['USD'].get(year, 2.85)
    else:
        converted = amount  # Same currency
    
    result = {
        "amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "year": year,
        "converted_amount": converted,
        "exchange_rate": converted / amount if amount != 0 else 0,
    }
    
    logger.info(f"Currency conversion result: {converted:.2f} {to_currency}")
    return result


def calculate_interest_impact(principal: float, years: int, start_year: int, scenario: str = "baseline") -> dict:
    """
    Calculate the impact of interest rates on an investment or loan.
    
    Args:
        principal: Initial amount in TND
        years: Number of years
        start_year: Starting year
        scenario: "optimistic", "baseline", or "pessimistic"
    
    Returns:
        Dictionary with interest impact details
    """
    logger.info(f"Calculating interest impact: {principal} TND over {years} years from {start_year}, scenario: {scenario}")
    
    if start_year < 2010 or start_year > 2026:
        raise ValueError("start_year must be between 2010 and 2026")
    
    if years <= 0:
        raise ValueError("years must be greater than 0")
    
    # Get average interest rate for the period
    years_range = list(range(start_year, min(start_year + years, 2027)))
    interest_rates = [CENTRAL_BANK_RATES.get(year, 7.0) for year in years_range]
    avg_rate = sum(interest_rates) / len(interest_rates) if interest_rates else 7.0
    
    # Apply scenario modifiers
    scenario_modifiers = {
        "optimistic": 0.7,  # Lower interest rates (good for borrowers)
        "baseline": 1.0,
        "pessimistic": 1.3,  # Higher interest rates (bad for borrowers)
    }
    
    modifier = scenario_modifiers.get(scenario, 1.0)
    annual_rate = (avg_rate * modifier) / 100
    
    # Calculate compound interest
    final_amount = principal * ((1 + annual_rate) ** years)
    total_interest = final_amount - principal
    
    # Year-by-year breakdown
    yearly_breakdown = {start_year: principal}
    current_amount = principal
    
    for i, year in enumerate(range(start_year + 1, start_year + years + 1), 1):
        if year > 2026:
            break
        current_amount *= (1 + annual_rate)
        yearly_breakdown[year] = current_amount
    
    result = {
        "principal": principal,
        "years": years,
        "start_year": start_year,
        "scenario": scenario,
        "average_rate": avg_rate * modifier,
        "final_amount": final_amount,
        "total_interest": total_interest,
        "interest_percentage": (total_interest / principal) * 100 if principal != 0 else 0,
        "yearly_breakdown": yearly_breakdown,
    }
    
    logger.info(f"Interest impact result: {final_amount:.2f} TND ({total_interest:.2f} TND interest)")
    return result


def get_economic_summary(year: int) -> dict:
    """
    Get a summary of all economic indicators for a specific year.
    
    Args:
        year: Year to get summary for
    
    Returns:
        Dictionary with all economic indicators
    """
    logger.info(f"Getting economic summary for year {year}")
    
    if year < 2010 or year > 2026:
        raise ValueError("year must be between 2010 and 2026")
    
    summary = {
        "year": year,
        "gdp_growth_rate": GDP_GROWTH_RATES.get(year, 0),
        "unemployment_rate": UNEMPLOYMENT_RATES.get(year, 0),
        "central_bank_rate": CENTRAL_BANK_RATES.get(year, 0),
        "gdp_value": GDP_VALUES.get(year, 0),
        "exchange_rate_usd": EXCHANGE_RATES['USD'].get(year, 0),
        "exchange_rate_eur": EXCHANGE_RATES['EUR'].get(year, 0),
    }
    
    logger.info(f"Economic summary for {year}: GDP growth {summary['gdp_growth_rate']}%, Unemployment {summary['unemployment_rate']}%")
    return summary
