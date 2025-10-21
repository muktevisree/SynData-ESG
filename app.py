import sys
import os
import streamlit as st
import pandas as pd
import yaml

# ✅ Add path to modules folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "modules")))

# ✅ Import your existing generator
from generator import generate_records
from ghg_rules import apply_ghg_rules

# ------------------- CONFIGURATION ------------------- #

SCHEMA_MAP = {
    "GHG": "presets/ghg.yaml"
}

st.set_page_config(page_title="SynData‑ESG Toolkit", layout="wide")
st.title("SynData‑ESG Toolkit")
st.caption("Synthetic ESG dataset generator aligned to OFP/OSDU schemas.")

# ------------------- SELECT DOMAIN ------------------- #

domain = st.selectbox("Select ESG Domain", list(SCHEMA_MAP.keys()))
schema_path = SCHEMA_MAP[domain]

# ------------------- LOAD YAML SCHEMA ------------------- #

def load_schema(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)

schema = load_schema(schema_path)

# ------------------- SYNTHETIC DATA GENERATION ------------------- #

st.subheader(f"🧪 Generate Synthetic {domain} Data")

row_count = st.slider("Number of synthetic rows to generate", 1, 500, 10)

if st.button("🚀 Generate Synthetic Data"):
    st.info("Generating synthetic data...")

    # Use your existing generator
    records = generate_records(schema, num_records=row_count)

    # Apply business logic / cleanup rules (optional)
    cleaned_records = []
    for rec in records:
        try:
            rec = apply_ghg_rules(rec)
        except Exception:
            pass  # skip if not applicable
        cleaned_records.append(rec)

    df = pd.DataFrame(cleaned_records)

    st.success(f"✅ Generated {len(df)} synthetic records!")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"synthetic_{domain.lower()}_data.csv",
        mime="text/csv",
    )

# ------------------- MANUAL ENTRY (OPTIONAL) ------------------- #

st.subheader(f"📝 Manual Data Entry – {domain} Schema")

def generate_blank_row(schema):
    return {field: "" for field in schema.keys()}

if "rows" not in st.session_state:
    st.session_state.rows = [generate_blank_row(schema)]

col1, col2 = st.columns(2)
if col1.button("➕ Add Row"):
    st.session_state.rows.append(generate_blank_row(schema))
if col2.button("🗑️ Clear All"):
    st.session_state.rows.clear()

manual_data = []
for i, row in enumerate(st.session_state.rows):
    with st.expander(f"Row {i+1}"):
        input_row = {}
        for field in schema.keys():
            input_row[field] = st.text_input(f"{field}", value=row.get(field, ""), key=f"{field}_{i}")
        manual_data.append(input_row)

if manual_data:
    df_manual = pd.DataFrame(manual_data)
    csv_manual = df_manual.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Manual Entry as CSV",
        data=csv_manual,
        file_name=f"manual_{domain.lower()}_data.csv",
        mime="text/csv",
    )
