# modules/ccs_rules.py

from datetime import datetime

def apply_ccs_rules(record):
    """
    Apply domain-specific logic to a CCS record.
    
    Args:
        record (dict): One generated row of data.
    
    Returns:
        dict: Cleaned and corrected record.
    """
    try:
        inject_start = datetime.strptime(record["injection_start_date"], "%Y-%m-%d")
        inject_end = datetime.strptime(record["injection_end_date"], "%Y-%m-%d")
        if inject_end <= inject_start:
            record["injection_end_date"] = inject_start.replace(year=inject_start.year + 1).strftime("%Y-%m-%d")
    except Exception as e:
        raise ValueError(f"Date error in record: {e}")

    try:
        co2 = float(record["co2_injected_tonnes"])
        ch4 = float(record["ch4_injected_tonnes"])
        n2o = float(record["n2o_injected_tonnes"])
        total = co2 + ch4 + n2o
        if ("total_ghg_injected_tonnes" not in record or 
                abs(float(record["total_ghg_injected_tonnes"]) - total) > 0.01):
            record["total_ghg_injected_tonnes"] = round(total, 2)
    except Exception as e:
        raise ValueError(f"GHG total error: {e}")

    return record


def validate_ccs_row(row):
    """
    Validate a row of CCS data. Returns list of error messages, or empty if valid.
    
    Args:
        row (pandas.Series or dict): The input row to validate.
    
    Returns:
        list: A list of string error messages.
    """
    errors = []

    try:
        inject_start = datetime.strptime(row["injection_start_date"], "%Y-%m-%d")
        inject_end = datetime.strptime(row["injection_end_date"], "%Y-%m-%d")
        if inject_end <= inject_start:
            errors.append("injection_end_date must be after injection_start_date")
    except Exception as e:
        errors.append(f"Date parsing error: {e}")

    try:
        co2 = float(row["co2_injected_tonnes"])
        ch4 = float(row["ch4_injected_tonnes"])
        n2o = float(row["n2o_injected_tonnes"])
        total = float(row["total_ghg_injected_tonnes"])
        if abs((co2 + ch4 + n2o) - total) > 0.01:
            errors.append("Total GHG mismatch (co2 + ch4 + n2o != total)")
    except Exception as e:
        errors.append(f"GHG parsing error: {e}")

    return errors
