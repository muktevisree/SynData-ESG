# app.py

import streamlit as st
import yaml
import os
import pandas as pd
import time
from datetime import datetime
from modules.schema_parser import load_schema
from modules.generator import generate_record

# ✅ Constants
SCHEMAS_DIR = "schema"
MAX_RECORDS = 1000
GENERATION_DELAY = 0.003  # Slight delay for UX fluidity

# ✅ Streamlit Page Settings
st.set_page_config(
    page_title="SynData-ESG Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧪 SynData-ESG: Synthetic Data Generator")

st.markdown("""
Welcome to the **SynData‑ESG Toolkit**.  
This app generates synthetic ESG datasets aligned with **Open Footprint (OFP)** and **Open Subsurface Data Universe (OSDU)** standards.

---

### 🧾 Expected Headers by ESG Domain:

**GHG (Greenhouse Gas Emissions)**:
- `facility_id`, `facility_name`, `country_code`, `latitude`, `longitude`
- `reporting_period_start`, `reporting_period_end`
- `scope_1_emissions_tonnes`, `scope_2_emissions_tonnes`, `total_emissions_tonnes`

**CCS (Carbon Capture and Storage)**:
- `facility_id`, `country_code`, `capture_source_type`, `storage_type`
- `co2_captured_tonnes`, `co2_stored_tonnes`, `total_cost_million_usd`

*(UHS and others coming soon!)*

---
""")

# ⚙️ Sidebar
st.sidebar.header("⚙️ Configuration")

available_schemas = [
    f.replace(".yaml", "") for f in os.listdir(SCHEMAS_DIR) if f.endswith(".yaml")
]
selected_schema = st.sidebar.selectbox("Select ESG Domain", available_schemas)

num_records = st.sidebar.slider(
    "Number of records to generate", min_value=10, max_value=MAX_RECORDS, step=10, value=100
)

generate_btn = st.sidebar.button("🚀 Generate Data")

# 📂 Load selected schema YAML
schema_file = os.path.join(SCHEMAS_DIR, f"{selected_schema}.yaml")
with open(schema_file, "r") as f:
    schema_yaml = yaml.safe_load(f)

schema = load_schema(schema_file)

st.subheader("📄 Schema Preview")
st.json(schema_yaml, expanded=False)

# ✅ Data Generation
if generate_btn:
    with st.spinner(f"⏳ Generating {num_records} synthetic records for '{selected_schema}'..."):
        placeholder = st.empty()
        placeholder.info(f"🔄 Generating {num_records} synthetic records for **{selected_schema}**...")

        progress_bar = st.progress(0, text="Starting...")

        records = []
        for i in range(num_records):
            record = generate_record(schema)

            # ⚙️ Calculated fields
            for field, spec in schema_yaml.items():
                if "calculated" in spec:
                    formula = spec["calculated"]
                    parts = formula.split("+")
                    if len(parts) == 2:
                        f1 = parts[0].strip()
                        f2 = parts[1].strip()
                        if f1 in record and f2 in record:
                            record[field] = record[f1] + record[f2]

            records.append(record)
            progress_bar.progress((i + 1) / num_records, text=f"Generating... {i+1}/{num_records}")
            time.sleep(GENERATION_DELAY)

        progress_bar.empty()
        placeholder.success(f"✅ Finished generating {num_records} records for **{selected_schema.upper()}**.")

    # 🧾 Create DataFrame
    df = pd.DataFrame(records)

    st.subheader("📊 Generated Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    # 📥 Export CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_filename = f"synthetic_data_{selected_schema}_{timestamp}.csv"

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv, output_filename, "text/csv")

    st.success(f"📁 File **{output_filename}** is ready for download!")

    # 🔔 Optional sound
    st.markdown("""
    <script>
        var audio = new Audio('https://www.soundjay.com/buttons/sounds/button-3.mp3');
        audio.play();
    </script>
    """, unsafe_allow_html=True)

    st.info(f"📦 Generated {len(df)} records for **{selected_schema.upper()}** schema.")
