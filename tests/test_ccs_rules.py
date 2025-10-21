from modules.ccs_rules import generate_valid_ccs_row

def test_generate_valid_ccs_row():
    row = generate_valid_ccs_row()
    assert row["co2_injected_tonnes"] <= row["co2_captured_tonnes"]
    assert row["injection_start_date"] < row["injection_end_date"]
    assert row["country_code"] in ["US", "IN", "DE", "BR", "AU"]
    assert isinstance(row["avg_injection_pressure_MPa"], float)
    assert isinstance(row["baseline_co2_ppm"], float)
    assert row["co2_leakage_detected"] in ["Yes", "No"]
