#!/usr/bin/env python3
"""
Script synopsis.
# :example
conda activate j2a_v2
python -m dataframe2csv
"""

import functiontransformations
import pandas as pd
from termcolor import colored

print(colored("Start", "blue"))
print(colored("Functions done", "green"))

# region transformations

# Path to the csv file generated from Jira
file_path = "docs/Jira2Dataframe.csv"

# Create a Data Frame
df = pd.read_csv(file_path)

# Path to the JSON file containing new rows
jsonfilepath = "standard_rows.json"

# Create a new DataFrame with desired columns
new_df = create_new_dataframe(df)

print(colored("Transformations done", "green"))
# endregion


# region processes
# Sort 'new_df' by the 'Title 3' column
new_df.sort_values(by="Title 3", inplace=True)

# Reset the index if needed
new_df.reset_index(drop=True, inplace=True)

# Filtering the data
filtered_df = delete_rows_with_empty_work_item_type(new_df)

# Update "Acceptance Criteria" for empty values
updated_df = update_acceptance_criteria(filtered_df)

# Processing DataFrame
create_fea_rows_df = create_feature_rows(updated_df)
delete_df = delete_title3_for_user_stories(create_fea_rows_df)

# Call the function to add new rows from the JSON file
dataframe_add_rows = add_rows_to_dataframe(create_fea_rows_df, jsonfilepath)

# Change the names for ADO
change_names(dataframe_add_rows)

# Create a copy of df
dataframe_later = dataframe_add_rows.copy()

# Save 'newest_df' to a CSV file without the "State 2" column
dataframe_add_rows.drop(columns=["State 2"], inplace=True)
dataframe_add_rows.drop(columns=["End Date"], inplace=True)
dataframe_add_rows.to_csv("docs/First.csv", index=False)
print(colored("First.csv done", "yellow"))

# Change the status
change_status(dataframe_later)

# Apply the custom function to update the "Resolved Date" column

update_dates_based_on_status_resolve(dataframe_later)
update_dates_based_on_status_target(dataframe_later)

update_iteration_path(dataframe_later)

# Create a updated file 'last_df.csv'
dataframe_later["State"] = dataframe_later["State 2"]
dataframe_later.drop(columns=["State 2"], inplace=True)
dataframe_later.drop(columns=["End Date"], inplace=True)

dataframe_feature_start_dates = update_feature_start_dates(dataframe_later)
dataframe_feature_target_dates = update_feature_target_dates(
    dataframe_feature_start_dates
)
dataframe_feature_state = update_feature_state(dataframe_feature_target_dates)
# Save the copy to a CSV file
# dataframe_later.to_csv("docs/dataframe_later.csv", index=False)
# dataframe_feature_start_dates.to_csv("docs/feature_start_dates.csv", index=False)
# dataframe_feature_target_dates.to_csv("docs/feature_target_dates.csv", index=False)
dataframe_feature_state.to_csv("docs/Second.csv", index=False)
print(colored("Second.csv done", "yellow"))
# endregion

print(colored("Finished", "blue"))
