# app.py

import streamlit as st
import yaml
import os
import pandas as pd

from modules.schema_parser import load_schema
from modules.generator import generate_records

SCHEMAS_DIR = "schemas"
OUTPUT_FILE = "synthetic_output.csv"

st.set_page_config(
    page_title="SynData-ESG Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧪 SynData-ESG: Synthetic Data Generator")

st.markdown("""
Welcome to the **SynData-ESG Toolkit**. This app generates synthetic data aligned to ESG domains
based on Open Footprint (OFP) and Open Subsurface Data Universe (OSDU) schemas.

🔍 Choose a domain, load its schema, and generate up to **1000** synthetic records with accurate
data types, ranges, and business rules.

📥 The generated data will be available for download as a CSV file.

---

### 🧾 Expected Headers (by ESG Domain)

**GHG (Greenhouse Gas Emissions)**:
- `facility_id`, `facility_name`, `country_code`, `latitude`, `longitude`
- `reporting_period_start`, `reporting_period_end`
- `scope_1_emissions_tonnes`, `scope_2_emissions_tonnes`, `total_emissions_tonnes`

*(CCS, UHS, etc. to be added in future releases)*

---
""")

# Sidebar – schema and record selection
st.sidebar.header("⚙️ Configuration")

available_schemas = [f.replace(".yaml", "") for f in os.listdir(SCHEMAS_DIR) if f.endswith(".yaml")]
selected_schema = st.sidebar.selectbox("Select ESG Domain", available_schemas)

num_records = st.sidebar.slider("Number of records to generate", min_value=10, max_value=1000, step=10, value=100)

generate_btn = st.sidebar.button("🚀 Generate Data")

# Load and display schema details
schema_file = os.path.join(SCHEMAS_DIR, f"{selected_schema}.yaml")
with open(schema_file, "r") as f:
    schema_yaml = yaml.safe_load(f)

schema = load_schema(schema_yaml)

st.subheader("📄 Schema Preview")
st.json(schema_yaml, expanded=False)

# Generate Data
if generate_btn:
    st.success(f"Generating {num_records} synthetic records for '{selected_schema}'...")
    data = generate_records(schema, num_records=num_records)
    df = pd.DataFrame(data)

    # Fill calculated fields (basic support for + operation)
    for field, spec in schema_yaml.items():
        if "calculated" in spec:
            formula = spec["calculated"]
            parts = formula.split("+")
            if len(parts) == 2:
                f1 = parts[0].strip()
                f2 = parts[1].strip()
                if f1 in df.columns and f2 in df.columns:
                    df[field] = df[f1] + df[f2]

    # Show and allow download
    st.subheader("📊 Generated Data Preview")
    st.dataframe(df.head())

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv, OUTPUT_FILE, "text/csv")
