"""
python -m transform_csv.py
"""

import pandas as pd

file_path = "docs/get_multiple_projects_jira_records_to_csv_2.csv"
df = pd.read_csv(file_path)

# Create a new DataFrame with desired columns
new_columns = [
    "ID",
    "Work Item Type",
    "Title 1",
    "Title 2",
    "Title 3",
    "Title 4",
    "Assigned To",
    "State",
    "Iteration Path",
    "Area Path",
    "Description",
    "Acceptance Criteria",
    "PG Business Value",
    "Value Area",
    "Work Category",
    "Tags",
    "Start Date",
    "Resolved Date",
]

new_df = pd.DataFrame(columns=new_columns)

# Populate the new DataFrame with data from the original DataFrame
for index, row in df.iterrows():
    new_row = {
        "ID": row["Issue ID"],
        "Work Item Type": row["Issue Type"],
        "Title 1": row["Summary"],
        "Assigned To": row["Assignee"],
        "State": row["Status"],
        "Iteration Path": row["Project name"],
        "Area Path": row["Project type"],
        "Description": row["Description"],
        "PG Business Value": row["Business Value [MM$]"],
        "Value Area": row["Custom field (Value)"],
        "Work Category": row["Custom field (Category)"],
        "Start Date": row["Created"],
        "Resolved Date": row["Resolved"],
    }
    new_df = new_df.append(new_row, ignore_index=True)

# Save the new DataFrame to a CSV file
new_df.to_csv("modified_file.csv", index=False)
