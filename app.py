import streamlit as st
import pandas as pd
from modules.schema_parser import load_schema
from modules.generator import generate_record
from modules.ghg_rules import apply_ghg_rules

import random
import yaml

# Page title
st.title("🧪 SynData-ESG: Synthetic ESG Dataset Generator")

# Sidebar
st.sidebar.header("⚙️ Generation Settings")
record_count = st.sidebar.number_input("Number of records", min_value=1, max_value=1000, value=10)

# Load schema
with open("presets/ghg.yaml", "r") as f:
    schema = yaml.safe_load(f)

# Generate button
if st.sidebar.button("Generate Dataset"):
    st.info("Generating synthetic GHG dataset...")
    data = []
    for _ in range(record_count):
        row = generate_record(schema)
        row = apply_ghg_rules(row)
        data.append(row)

    df = pd.DataFrame(data)
    st.success(f"✅ Generated {record_count} records.")

    # Show preview
    st.dataframe(df)

    # Download link
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", data=csv, file_name="synthetic_ghg_data.csv", mime="text/csv")

else:
    st.markdown("⬅️ Use the sidebar to generate synthetic GHG emissions data.")
