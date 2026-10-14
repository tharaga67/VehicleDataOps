# VehicleDataOps
## Automotive Manufacturing Data Engineering & Quality Dashboard

VehicleDataOps is a small data engineering portfolio project that demonstrates how factory production records can be processed, validated, stored, and explored through an interactive dashboard.

**Technology stack:** Python, Pandas, SQL, SQLite, Streamlit

> **Dataset note:** The repository includes synthetic demonstration data. It is not real Tata Motors data or data from any other manufacturer.

## Project workflow

1. **Extract:** Read production records from a CSV file using Pandas.
2. **Transform:** Standardize text fields, convert data types, handle missing values, and calculate defect-rate metrics.
3. **Validate:** Check for duplicate record IDs and flag invalid measurements.
4. **Load:** Store the processed records in a SQLite table.
5. **Analyze:** Summarize production volume, defects, defect rate, and quality status by production line.
6. **Visualize:** Use an interactive Streamlit dashboard to filter records, inspect metrics, and download processed data.

## Key features

- CSV-based data ingestion
- Data cleaning and missing-value handling
- Duplicate record checks and basic validation rules
- Derived defect-rate and quality-status fields
- SQLite data storage
- Production-line and quality-status filters
- Summary charts and downloadable processed records

## Run locally

Python 3.11 or 3.12 is recommended.

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

The application should open in your browser at the local Streamlit address shown in the terminal.

## Deploy

The application can be deployed from this GitHub repository using Streamlit Community Cloud.

1. Sign in to Streamlit Community Cloud with GitHub.
2. Create an app and select this repository and the `main` branch.
3. Set the main file path to `app.py`.
4. Deploy and verify the app after startup.

Deployment guide: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app

## Repository structure

```text
VehicleDataOps/
├── app.py
├── requirements.txt
├── README.md
└── data/
    └── factory_production.csv
```

## Scope and limitations

This is a portfolio demonstration of a small batch ETL workflow. It uses synthetic data and simple validation rules; it is not a production manufacturing system and does not establish real-world failure predictions. The project can be extended with a real, appropriately licensed dataset, additional SQL analysis, automated tests, and more detailed data-quality reporting.
