# modules/ghg_rules.py

from datetime import datetime

def apply_ghg_rules(record):
    """
    Apply domain-specific logic to a GHG record.
    
    Args:
        record (dict): One generated row of data.
    
    Returns:
        dict: Cleaned and corrected record.
    """
    # Ensure start date is before end date
    try:
        start = datetime.strptime(record["reporting_period_start"], "%Y-%m-%d")
        end = datetime.strptime(record["reporting_period_end"], "%Y-%m-%d")
        if end <= start:
            record["reporting_period_end"] = start.replace(year=start.year + 1).strftime("%Y-%m-%d")
    except Exception as e:
        raise ValueError(f"Date error in record: {e}")

    # Calculate total emissions if not already set or mismatch
    try:
        scope_1 = float(record["scope_1_emissions_tonnes"])
        scope_2 = float(record["scope_2_emissions_tonnes"])
        expected_total = scope_1 + scope_2
        if ("total_emissions_tonnes" not in record or 
                abs(float(record["total_emissions_tonnes"]) - expected_total) > 0.01):
            record["total_emissions_tonnes"] = round(expected_total, 2)
    except Exception as e:
        raise ValueError(f"Emission total error: {e}")

    return record


def validate_ghg_row(row):
    """
    Validate a row of GHG data. Returns list of error messages, or empty if valid.
    
    Args:
        row (pandas.Series or dict): The input row to validate.
    
    Returns:
        list: A list of string error messages.
    """
    errors = []

    try:
        # Validate date logic
        start = datetime.strptime(row["reporting_period_start"], "%Y-%m-%d")
        end = datetime.strptime(row["reporting_period_end"], "%Y-%m-%d")
        if end <= start:
            errors.append("reporting_period_end must be after reporting_period_start")
    except Exception as e:
        errors.append(f"Date parsing error: {e}")

    try:
        scope_1 = float(row["scope_1_emissions_tonnes"])
        scope_2 = float(row["scope_2_emissions_tonnes"])
        total = float(row["total_emissions_tonnes"])
        if abs((scope_1 + scope_2) - total) > 0.01:
            errors.append("Total emissions mismatch (scope_1 + scope_2 != total)")
    except Exception as e:
        errors.append(f"Emission parsing error: {e}")

    return errors
