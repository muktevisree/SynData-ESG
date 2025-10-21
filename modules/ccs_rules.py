
import random
import uuid
from datetime import datetime, timedelta


def generate_valid_ccs_row():
    start_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))
    end_date = start_date + timedelta(days=random.randint(30, 180))
    captured = round(random.uniform(5000, 20000), 2)
    injected = round(captured * random.uniform(0.9, 1.0), 2)

    return {
        "facility_id": str(uuid.uuid4())[:8],
        "country_code": random.choice(["US", "IN", "DE", "BR", "AU"]),
        "lat": round(random.uniform(-90, 90), 6),
        "lon": round(random.uniform(-180, 180), 6),
        "well_id": str(uuid.uuid4())[:10],
        "injection_start_date": start_date.strftime("%Y-%m-%d"),
        "injection_end_date": end_date.strftime("%Y-%m-%d"),
        "co2_injected_tonnes": injected,
        "co2_captured_tonnes": captured,
        "co2_leakage_detected": random.choice(["Yes", "No"]),
        "monitoring_frequency": random.choice(["Monthly", "Quarterly", "Annual"]),
        "baseline_co2_ppm": round(random.uniform(350, 420), 2),
        "avg_injection_pressure_MPa": round(random.uniform(8.0, 25.0), 2),
        "avg_injection_temp_C": round(random.uniform(20.0, 60.0), 2),
    }

