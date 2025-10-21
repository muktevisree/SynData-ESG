import streamlit as st
import pandas as pd
import yaml
import os
from modules.ghg_rules import validate_ghg_row
from modules.ccs_rules import validate_ccs_row
from modules.uhs_rules import validate_uhs_row

# Map domain to schema and rule function
DOMAIN_MAP = {
    "GHG": {
        "schema": "presets/ghg.yaml",
        "validator": validate_ghg_row
    },
    "CCS": {
        "schema": "presets/ccs.yaml",
        "validator": validate_ccs_row
    },
    "UHS": {
        "schema": "presets/uhs.yaml",
        "validator": validate_uhs_row
    }
}

st.set_page_config(page_title="SynData-ESG Toolkit", layout="wide")
st.title("SynData-ESG Toolkit")

# Select ESG domain
domain = st.selectbox("Select ESG Domain", list(DOMAIN_MAP.keys()))

# Load schema and validator
schema_path = DOMAIN_MAP[domain]["schema"]
validator = DOMAIN_MAP[domain]["validator"]

# Load schema
def load_schema(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

# Generate blank row based on schema
def generate_blank_row(schema):
    return {field['name']: '' for field in schema['fields']}

schema = load_schema(schema_path)

st.subheader(f"Upload CSV for {domain} Validation")
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    errors = []
    for idx, row in df.iterrows():
        row_errors = validator(row)
        if row_errors:
            errors.append({"Row": idx + 2, "Errors": "; ".join(row_errors)})

    if errors:
        st.error("Validation Errors Found")
        st.dataframe(pd.DataFrame(errors))
    else:
        st.success("No Validation Errors! 🎉")

st.subheader(f"Manual Data Entry – {domain} Schema")
if "rows" not in st.session_state:
    st.session_state.rows = [generate_blank_row(schema)]

# Add/Remove rows buttons
col1, col2 = st.columns([1, 1])
if col1.button("➕ Add Row"):
    st.session_state.rows.append(generate_blank_row(schema))
if col2.button("🗑️ Clear All"):
    st.session_state.rows.clear()

# Input form
data = []
for i, row in enumerate(st.session_state.rows):
    with st.expander(f"Row {i+1}"):
        input_row = {}
        for field in schema['fields']:
            fname = field['name']
            ftype = field.get('type', 'string')
            default_val = row.get(fname, '')
            if ftype in ['number', 'float', 'integer']:
                input_row[fname] = st.number_input(f"{fname}", value=float(default_val) if default_val else 0.0, key=f"{fname}_{i}")
            else:
                input_row[fname] = st.text_input(f"{fname}", value=str(default_val), key=f"{fname}_{i}")
        data.append(input_row)

# Download button
if data:
    df_out = pd.DataFrame(data)
    csv = df_out.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"synthetic_{domain.lower()}_data.csv",
        mime='text/csv')
