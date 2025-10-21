import pytest
from modules.ccs_rules import generate_ccs_row

def test_generate_ccs_row_structure():
    row = generate_ccs_row()
    expected_fields = [
        "facility_id", "country_code", "lat", "lon", "capture_tech",
        "co2_captured_tonnes", "co2_purified_tonnes", "pipeline_length_km",
        "transport_mode", "injection_well_id", "injection_start_date",
        "injection_end_date", "co2_injected_tonnes", "storage_reservoir_type",
        "avg_reservoir_pressure_MPa", "avg_reservoir_temp_C",
        "monitoring_method", "co2_leakage_estimate_tonnes"
    ]
    for field in expected_fields:
        assert field in row
