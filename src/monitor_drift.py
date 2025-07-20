import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

# Load data
ref_data = pd.read_csv("data/raw_data.csv").tail(300)
curr_data = pd.read_csv("data/raw_data.csv").tail(100)

# Create report
report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=ref_data, current_data=curr_data)

# Save to multiple formats
report.save_html("reports/data_drift_report.html")
report.save_json("reports/data_drift_report.json")

# Optional: Save as dict
report_dict = report.as_dict()
