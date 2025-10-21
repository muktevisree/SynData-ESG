import sys
import os
import streamlit as st
import pandas as pd
import yaml

# 👇 Adjust sys.path for local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules')))

from ghg_rules import apply_ghg_rules
from generator import generate_ghg_data

# ------------------- CONFIGURATION ------------------- #

SCHEMA_MAP = {
    "GHG": "presets/ghg.yaml"
}

st.set_page_config(page_title="SynData-ESG Toolkit", layout="wide")
st.title("SynData-ESG Toolkit")

# ------------------- DOMAIN SELECTION ------------------- #

domain = st.selectbox("Select ESG Domain", list(SCHEMA_MAP.keys()))
schema_path = SCHEMA_MAP[domain]

# ------------------- SCHEMA LOADER ------------------- #

def load_schema(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

schema = load_schema(schema_path)

# ------------------- SYNTHETIC GENERATOR ------------------- #

st.subheader(f"🧪 Generate Synthetic {domain} Data")
row_count = st.slider("Number of synthetic rows", min_value=1, max_value=100, value=10)

if st.button("🚀 Generate Synthetic Data"):
    synthetic_data = generate_ghg_data(schema, row_count)
    
    # Apply optional rules/cleanup
    cleaned_data = []
    for record in synthetic_data:
        try:
            record = apply_ghg_rules(record)
        except Exception as e:
            st.warning(f"⚠️ Issue in record: {e}")
        cleaned_data.append(record)
    
    df = pd.DataFrame(cleaned_data)
    st.success(f"✅ Generated {len(df)} synthetic records!")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"synthetic_{domain.lower()}_data.csv",
        mime='text/csv'
    )

# ------------------- MANUAL DATA ENTRY ------------------- #

st.subheader(f"📝 Manual Data Entry – {domain} Schema")

def generate_blank_row(schema):
    return {field_name: '' for field_name in schema.keys()}

if "rows" not in st.session_state:
    st.session_state.rows = [generate_blank_row(schema)]

col1, col2 = st.columns([1, 1])
if col1.button("➕ Add Row"):
    st.session_state.rows.append(generate_blank_row(schema))
if col2.button("🗑️ Clear All"):
    st.session_state.rows.clear()

# Input form
data = []
for i, row in enumerate(st.session_state.rows):
    with st.expander(f"Row {i+1}", expanded=False):
        input_row = {}
        for field_name in schema.keys():
            default_val = row.get(field_name, '')
            input_row[field_name] = st.text_input(
                label=f"{field_name}",
                value=str(default_val),
                key=f"{field_name}_{i}"
            )
        data.append(input_row)

# ------------------- CSV DOWNLOAD ------------------- #

if data:
    df_out = pd.DataFrame(data)
    csv = df_out.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Manual Entry as CSV",
        data=csv,
        file_name=f"manual_{domain.lower()}_data.csv",
        mime='text/csv'
    )
