# SynData-ESG

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Made With Faker](https://img.shields.io/badge/made%20with-faker-orange)](https://faker.readthedocs.io/)
[![Streamlit UI](https://img.shields.io/badge/Streamlit-Available-green)](https://streamlit.io/)
[![DOI](https://zenodo.org/badge/DOI/YOUR_DOI_HERE.svg)](https://doi.org/YOUR_DOI_HERE)

---

## 🔍 Overview

**SynData-ESG** is an open-source synthetic data generation toolkit purpose-built for environmental, social, and governance (ESG) data applications. It allows researchers, developers, and ESG analysts to generate reproducible datasets for:

- 🌍 **GHG Emissions** (Scope 1, 2, and Total CO₂e)
- 🧊 **Carbon Capture and Storage (CCS)**
- 💧 **Underground Hydrogen Storage (UHS)**
- 🚰 Future-ready: **Water, Air, Waste, and Social** domains

All data generation is aligned to **Open Footprint (OFP)** and **Open Subsurface Data Universe (OSDU)** schema standards, ensuring compatibility with ESG pipelines, analytics platforms, and digital twin environments.

---

## ⚙️ Features

- ✅ **YAML-based schema-driven generation**
- 🎛️ Faker-powered simulation for realistic entities (facilities, countries, emissions, dates)
- 🔁 Built-in **domain rules** (e.g., start < end, total = scope1 + scope2)
- 🧪 Unit tested CLI + Modules
- 🧵 Streamlit cloud UI (optional)
- 🧾 JOSS publication-ready
- 📂 Reproducible with fixed random seed

---

## 📁 Folder Structure

```
SynData-ESG/
├── cli/
│   └── generate_synthetic.py
├── modules/
│   ├── generator.py
│   ├── schema_parser.py
│   └── ghg_rules.py
├── presets/
│   └── ghg.yaml
├── examples/
│   └── sample_ghg.csv
├── tests/
│   └── test_generator.py
├── paper/
│   ├── paper.md
│   └── paper.bib
├── LICENSE
├── README.md
├── CONTRIBUTING.md
└── requirements.txt
```

---

## 🚀 Quick Start

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/SynData-ESG.git
cd SynData-ESG
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate Data from GHG Schema

```bash
python cli/generate_synthetic.py --schema presets/ghg.yaml --output examples/synthetic_ghg.csv --num-records 100
```

---

## 📦 Sample Output

| facility_id | facility_name | country_code | latitude | longitude | scope_1_emissions_tonnes | scope_2_emissions_tonnes | total_emissions_tonnes |
|-------------|---------------|---------------|----------|-----------|---------------------------|---------------------------|--------------------------|
| 0c1f...     | GreenCo Ltd.  | US            | 40.7128  | -74.0060  | 51234.0                   | 10000.0                   | 61234.0                  |

---

## 🧾 Sample Schema (presets/ghg.yaml)

```yaml
facility_id:
  type: string
  generator: uuid

country_code:
  type: string
  values: ["US", "IN", "CN", "DE", "BR"]

scope_1_emissions_tonnes:
  type: float
  min: 1000
  max: 1000000

scope_2_emissions_tonnes:
  type: float
  min: 100
  max: 500000

total_emissions_tonnes:
  type: float
  calculated: scope_1_emissions_tonnes + scope_2_emissions_tonnes
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 🧵 Streamlit Web App (Coming Soon)

A Streamlit-based UI will allow interactive schema selection and record generation. Stay tuned!

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙌 Citation

> Muktevi, S. (2025). *SynData-ESG: Synthetic ESG Dataset Generator* (v0.1.0) [Software]. Zenodo. https://doi.org/YOUR_DOI_HERE

---

## 👤 Author

**Sreekanth Muktevi**  
[LinkedIn](https://www.linkedin.com/in/sreemuktevi) | [ORCID](https://orcid.org/0009-0007-8116-3176)  
Vice President, YASH Technologies  
Sustainability & Digital Innovation Leader

---

## 📣 Acknowledgements

- Open Footprint Forum (OFP)
- OSDU Forum
- IEEE Data Descriptions
- ESG-Disclose.com
- JOSS

---

## 🤝 Contributions

Pull requests are welcome. For major changes, please open an issue first.  
See [`CONTRIBUTING.md`](CONTRIBUTING.md) for details.

---

## 📊 Metrics & Adoption

- ⭐ GitHub Stars/Forks
- 📥 Zenodo DOI downloads
- 📈 Streamlit usage stats (if public)
- 🗞️ JOSS citation impact
- 🧑‍💻 Google Scholar citations

Let us know how you're using SynData-ESG!