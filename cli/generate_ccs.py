import csv
import random
import argparse
from modules.ccs_rules import generate_valid_ccs_row


def generate_ccs_dataset(output_path: str, num_rows: int = 100):
    headers = [
        "facility_id", "country_code", "lat", "lon",
        "well_id", "injection_start_date", "injection_end_date",
        "co2_injected_tonnes", "co2_captured_tonnes", "co2_leakage_detected",
        "monitoring_frequency", "baseline_co2_ppm", "avg_injection_pressure_MPa",
        "avg_injection_temp_C"
    ]
    with open(output_path, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for _ in range(num_rows):
            row = generate_valid_ccs_row()
            writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic CCS dataset")
    parser.add_argument("--output", default="examples/synthetic_ccs_data.csv")
    parser.add_argument("--rows", type=int, default=100)
    args = parser.parse_args()

    generate_ccs_dataset(args.output, args.rows)
    print(f"✅ CCS dataset written to {args.output}")


if __name__ == "__main__":
    main()
