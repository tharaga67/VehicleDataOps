# VehicleDataOps
### Automotive Manufacturing Data Engineering & Quality Dashboard

VehicleDataOps is a beginner-friendly portfolio project demonstrating an end-to-end data workflow on **synthetic factory production data**. It is designed to be easy to run, explain, customize, and deploy.

## What it demonstrates
- **Extract:** Read factory production records from CSV using Pandas.
- **Transform:** Standardize text fields, convert data types, handle missing values, and derive defect-rate metrics.
- **Validate:** Detect duplicate IDs and flag invalid measurements.
- **Load:** Load the processed dataset into a SQLite table.
- **Analyze:** Summarize production volume, defects, defect rate, and quality status by production line.
- **Present:** Explore and filter results in an interactive Streamlit dashboard; download processed records.

> Important: The included dataset is synthetic and is not real Tata Motors or other manufacturer data.

## Run locally
Recommended: Python 3.11 or 3.12.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Deploy a public demo
1. Create a GitHub repository named `VehicleDataOps`.
2. Upload the contents of this folder to your repository (keep `app.py`, `requirements.txt`, and `data/factory_production.csv`).
3. Sign in to Streamlit Community Cloud with GitHub: https://share.streamlit.io/
4. Choose **Create app**, select your repository and branch, and set the main file path to `app.py`.
5. Deploy. Streamlit will give you your own public `*.streamlit.app` URL.
6. Open that URL in a private/incognito window to verify it works before putting it on your resume.

Official deployment guide: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app

## Suggested resume entry (use only after you have run and verified it)
**VehicleDataOps — Automotive Manufacturing Data Engineering Dashboard** | Python, Pandas, SQL (SQLite), Streamlit
- Built a CSV-to-SQLite ETL workflow to clean, validate, and transform synthetic factory production records.
- Implemented missing-value handling, duplicate-ID checks, quality flags, and defect-rate calculations.
- Developed an interactive dashboard to analyze production, defects, and quality status by production line.

## Make it genuinely yours
- Change the dashboard design and add at least one feature of your own.
- Add a short `docs/architecture.png` or architecture section to the README.
- Write a few SQL queries and explain the results.
- Add screenshots and document what you tested.
- Be prepared to explain every line and every metric in an interview.

## Repository structure
```text
VehicleDataOps/
├── app.py
├── requirements.txt
├── README.md
└── data/
    └── factory_production.csv
```
