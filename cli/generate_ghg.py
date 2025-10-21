# cli/generate_synthetic.py

import argparse
import os
import sys
import pandas as pd

# Add root to sys.path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.schema_parser import load_schema
from modules.generator import generate_records
from modules.ghg_rules import apply_ghg_rules

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic ESG data from schema.")
    parser.add_argument("--schema", required=True, help="Path to YAML schema file (e.g., schema/ghg.yaml)")
    parser.add_argument("--records", type=int, default=100, help="Number of records to generate")
    parser.add_argument("--output", default="examples/sample_ghg.csv", help="Output CSV file path")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")

    args = parser.parse_args()

    print(f"📥 Loading schema: {args.schema}")
    schema = load_schema(args.schema)

    print(f"🔁 Generating {args.records} synthetic records...")
    records = generate_records(schema, args.records, args.seed)

    print("🧠 Applying GHG business rules...")
    updated_records = [apply_ghg_rules(record) for record in records]

    df = pd.DataFrame(updated_records)
    df.to_csv(args.output, index=False)

    print(f"✅ Done! Data saved to: {args.output}")

if __name__ == "__main__":
    main()
