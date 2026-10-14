import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "factory_production.csv"
DB_PATH = ROOT / "vehicledataops.db"

st.set_page_config(page_title="VehicleDataOps | Factory Quality", page_icon="🏭", layout="wide")

@st.cache_data
def load_raw_data():
    return pd.read_csv(DATA_PATH)

def run_etl(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Extract CSV, transform/validate fields, and load clean records into SQLite."""
    df = raw.copy()
    initial_rows = len(df)

    # Standardize text fields.
    for col in ["production_line", "component", "supplier"]:
        df[col] = df[col].astype("string").str.strip()

    # Convert types safely.
    df["production_date"] = pd.to_datetime(df["production_date"], errors="coerce")
    numeric_cols = [
        "units_produced", "defect_count", "downtime_minutes",
        "machine_temp_c", "hydraulic_pressure_bar"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Data quality checks.
    missing_before = int(df.isna().sum().sum())
    duplicate_rows = int(df.duplicated(subset=["record_id"]).sum())
    df = df.drop_duplicates(subset=["record_id"], keep="first")

    # Fill missing category values and numeric readings with transparent defaults.
    df["supplier"] = df["supplier"].fillna("").replace("", "Unknown Supplier")
    df["machine_temp_c"] = df["machine_temp_c"].fillna(df["machine_temp_c"].median())
    df["hydraulic_pressure_bar"] = df["hydraulic_pressure_bar"].fillna(
        df["hydraulic_pressure_bar"].median()
    )
    df["production_date"] = df["production_date"].fillna(pd.Timestamp("2026-01-01"))
    df["production_line"] = df["production_line"].fillna("Unknown Line")
    df["component"] = df["component"].fillna("Unknown Component")

    # Add derived metrics and business rules.
    df["defect_rate_pct"] = (df["defect_count"] / df["units_produced"].clip(lower=1) * 100).round(2)
    df["quality_status"] = df["defect_rate_pct"].apply(
        lambda x: "Review" if x >= 8 else ("Monitor" if x >= 5 else "Within Threshold")
    )
    df["data_quality_status"] = "PASS"
    invalid_mask = (
        (df["units_produced"] <= 0) |
        (df["defect_count"] < 0) |
        (df["downtime_minutes"] < 0) |
        (df["machine_temp_c"] < 0) |
        (df["hydraulic_pressure_bar"] < 0)
    )
    df.loc[invalid_mask, "data_quality_status"] = "CHECK"

    # Keep output types SQLite-friendly.
    df["production_date"] = df["production_date"].dt.strftime("%Y-%m-%d")
    stats = {
        "input_rows": initial_rows,
        "output_rows": len(df),
        "duplicate_ids_removed": duplicate_rows,
        "missing_cells_detected": missing_before,
        "rows_flagged_for_quality": int((df["data_quality_status"] == "CHECK").sum()),
    }

    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql("production_quality", conn, if_exists="replace", index=False)
        loaded_rows = conn.execute("SELECT COUNT(*) FROM production_quality").fetchone()[0]
    stats["rows_loaded_to_sqlite"] = int(loaded_rows)
    return df, stats

st.title("🏭 VehicleDataOps")
st.subheader("Automotive Manufacturing Data Engineering & Quality Dashboard")
st.caption("Demonstration project using synthetic factory data. Metrics are illustrative, not real manufacturer data.")

raw = load_raw_data()
processed, stats = run_etl(raw)

with st.sidebar:
    st.header("Pipeline controls")
    st.write("**Source:** `data/factory_production.csv`")
    st.write("**Target:** SQLite table `production_quality`")
    st.write("**Pipeline:** Extract → Transform → Validate → Load")
    line_options = ["All"] + sorted(processed["production_line"].dropna().unique().tolist())
    selected_line = st.selectbox("Production line", line_options)
    quality_options = ["All"] + sorted(processed["quality_status"].unique().tolist())
    selected_quality = st.selectbox("Quality status", quality_options)
    st.info("Refresh the browser to rerun the ETL pipeline.")

filtered = processed.copy()
if selected_line != "All":
    filtered = filtered[filtered["production_line"] == selected_line]
if selected_quality != "All":
    filtered = filtered[filtered["quality_status"] == selected_quality]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Production records", f"{len(filtered):,}")
c2.metric("Units produced", f"{int(filtered['units_produced'].sum()):,}")
c3.metric("Defects", f"{int(filtered['defect_count'].sum()):,}")
overall_rate = (filtered["defect_count"].sum() / max(filtered["units_produced"].sum(), 1)) * 100
c4.metric("Overall defect rate", f"{overall_rate:.2f}%")

st.divider()
left, right = st.columns(2)
with left:
    st.markdown("### Defects by production line")
    line_summary = filtered.groupby("production_line", as_index=False).agg(
        defects=("defect_count", "sum"), units=("units_produced", "sum")
    )
    if not line_summary.empty:
        st.bar_chart(line_summary.set_index("production_line")["defects"])
    else:
        st.info("No records for the selected filters.")

with right:
    st.markdown("### Quality status distribution")
    status_counts = filtered["quality_status"].value_counts()
    if not status_counts.empty:
        st.bar_chart(status_counts)
    else:
        st.info("No records for the selected filters.")

st.markdown("### ETL run & data-quality summary")
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Input rows", stats["input_rows"])
m2.metric("Output rows", stats["output_rows"])
m3.metric("Duplicate IDs removed", stats["duplicate_ids_removed"])
m4.metric("Missing cells detected", stats["missing_cells_detected"])
m5.metric("Rows flagged", stats["rows_flagged_for_quality"])

st.markdown("### Processed production data")
st.dataframe(filtered, use_container_width=True, hide_index=True)

csv_bytes = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered dataset (CSV)", data=csv_bytes,
                   file_name="vehicledataops_processed.csv", mime="text/csv")

with st.expander("View SQL table validation"):
    with sqlite3.connect(DB_PATH) as conn:
        loaded = pd.read_sql_query(
            "SELECT production_line, COUNT(*) AS records, SUM(units_produced) AS units, "
            "SUM(defect_count) AS defects, ROUND(AVG(defect_rate_pct), 2) AS avg_defect_rate_pct "
            "FROM production_quality GROUP BY production_line ORDER BY defects DESC",
            conn,
        )
    st.dataframe(loaded, use_container_width=True, hide_index=True)

st.caption("Built with Python, Pandas, SQLite, and Streamlit. Dataset is synthetic and included in the repository.")
