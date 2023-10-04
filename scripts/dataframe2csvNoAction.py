#!/usr/bin/env python3
"""
Script synopsis.
# :example
conda activate j2a_v2
python -m dataframe2csvNoAction
"""
import json

import pandas as pd
from termcolor import colored

current_date = pd.Timestamp.now()
print(colored("Start", "blue"))

# region functions


# Defining functions
def add_rows_to_dataframe(dataframe, jsonfilepath):
    """Read JSON data from the file"""
    with open(jsonfilepath, "r") as json_file:
        json_data = json.load(json_file)

    # Create a new DataFrame with the specified JSON data
    new_rows = pd.DataFrame(json_data)

    # Concatenate the new rows at the top of the original DataFrame
    dataframe = pd.concat([new_rows, dataframe], ignore_index=True)

    return dataframe


def delete_rows_with_empty_work_item_type(dataframe):
    """Use boolean indexing to filter rows where 'Work Item Type' is not empty"""
    filtered_dataframe = dataframe[dataframe["Work Item Type"] == "User story"]

    return filtered_dataframe


def create_feature_rows(dataframe):
    # Create an empty DataFrame to store the new rows
    new_rows_df = pd.DataFrame(columns=dataframe.columns)

    # Initialize the current_title variable
    current_title = None

    for _, row in dataframe.iterrows():  # Use _ to ignore the row index
        title_3 = row["Title 3"]

        if title_3 != current_title:
            # Create a new "Feature" row with the same "Title 3" value
            new_feature_row = {
                "ID": "",
                "Work Item Type": "Feature",
                "Title 1": "",
                "Title 2": "",
                "Title 3": title_3,
                "Title 4": "",
                "Assigned To": "Szymon Osiecki",
                "State": "New",
                "Iteration Path": "\\CSE\\CSE Solution Engineering",
                "Area Path": "\\AzureCSE\\SolutionEngineering",
                "Description": "",
                "Acceptance Criteria": "",
                "PG Business Value": "AI Factory Project delivery",
                "Value Area": "Business",
                "Work Category": "",
                "Tags": "EE-AIFactory",
                "Start Date": "",
                "Resolved Date": "",
            }
            new_feature_row_df = pd.DataFrame([new_feature_row])
            new_rows_df = pd.concat(
                [new_rows_df, new_feature_row_df], ignore_index=True
            )

            # Update the current_title
            current_title = title_3

        # Append the original row
        new_rows_df = pd.concat([new_rows_df, row.to_frame().T], ignore_index=True)

    return new_rows_df


def delete_title3_for_user_stories(dataframe):
    """Delete the value from "Title 3" for "User story" rows"""
    for index, row in dataframe.iterrows():
        if row["Work Item Type"] == "User story":
            dataframe.at[index, "Title 3"] = ""
    return dataframe


def change_names(dataframe):
    """Define a mapping of name changes"""
    name_mapping = {
        "Pawel Borowiak": "Borowiak, Pawel",
        "kamil gajek": "Kamil Gajek",
        "maciej znalezniak": "Maciej Znalezniak",
        "Aleksander Kamczyc": "Kamczyc, Aleksander Non-PG",
    }

    # Apply the name changes to the "Assigned To" column
    dataframe["Assigned To"] = (
        dataframe["Assigned To"].map(name_mapping).fillna(dataframe["Assigned To"])
    )

    # Return the updated DataFrame
    return dataframe


def change_status(dataframe):
    """Define a mapping of name changes"""
    status_mapping = {
        "Done": "Closed",
        "To Do": "New",
        "Review": "Under Review",
        "Blocked": "On Hold",
    }

    # Apply the name changes to the "Status 2" column
    dataframe["State 2"] = (
        dataframe["State 2"].map(status_mapping).fillna(dataframe["State 2"])
    )

    # Set "Status 2" to "Active" when "Work Item Type" is "Feature"
    dataframe.loc[dataframe["Work Item Type"] == "Feature", "State 2"] = "Active"

    # Return the updated DataFrame
    return dataframe


def change_status_backlog(dataframe):
    """Define a mapping of name changes"""
    status_mapping = {
        "Backlog": "New",
    }

    # Apply the name changes to the "Status 2" column
    dataframe["State 2"] = (
        dataframe["State 2"].map(status_mapping).fillna(dataframe["State 2"])
    )

    # Set "Status 2" to "Active" when "Work Item Type" is "Feature"
    dataframe.loc[dataframe["Work Item Type"] == "Feature", "State 2"] = "Active"

    # Return the updated DataFrame
    return dataframe


def change_backlog_to_new(dataframe, status_mapping):
    """Change values based on the status mapping"""
    if "State 2" in dataframe.columns:
        dataframe["State 2"] = (
            dataframe["State 2"].map(status_mapping).fillna(dataframe["State 2"])
        )
    # Apply the name changes to the "Status 2" column
    dataframe["State 2"] = (
        dataframe["State 2"].map(status_mapping).fillna(dataframe["State 2"])
    )

    # Set "Status 2" to "Active" when "Work Item Type" is "Feature"
    dataframe.loc[dataframe["Work Item Type"] == "Feature", "State 2"] = "Active"

    # Return the updated DataFrame
    return dataframe


# Function to update "Acceptance Criteria" for empty values
def update_acceptance_criteria(dataframe):
    """Create a copy of the DataFrame to avoid SettingWithCopyWarning"""
    dataframe_copy = dataframe.copy()
    # Fill missing values in the "Acceptance Criteria" column
    dataframe_copy["Acceptance Criteria"].fillna("User story completed", inplace=True)
    return dataframe_copy


def update_dates_based_on_status_resolve(dataframe):
    """Updating the resolve date column"""

    def calculate_date(row):
        status = row["State 2"]
        if status == "Closed":
            return row["End Date"]

    dataframe["Resolved Date"] = dataframe.apply(calculate_date, axis=1)
    dataframe["Target Date"] = dataframe["Resolved Date"]


def update_dates_based_on_status_target(dataframe):
    """Updating the target date column"""
    dataframe["End Date"] = ""

    def calculate_date(row):
        status = row["State 2"]
        if status == "Under Review":
            return current_date + pd.DateOffset(weeks=1)
        elif status == "In Progress":
            return current_date + pd.DateOffset(months=1)
        elif status == "New":
            return current_date + pd.DateOffset(months=2)
        elif status == "Backlog":
            return current_date + pd.DateOffset(months=3)
        else:
            return row["End Date"]

    dataframe["Target Date"] = dataframe.apply(calculate_date, axis=1)


def calculate_iteration_path(row):
    resolved_date = pd.to_datetime(row["Resolved Date"], errors="coerce")
    target_date = pd.to_datetime(row["Target Date"], errors="coerce")

    if not pd.isnull(resolved_date):
        month = resolved_date.strftime("%B")  # Get the month name
        year = str(resolved_date.year)[-2:]  # Get the last two digits of the year
        return f"\\CSE\\CSE Solution Engineering\\{month}'{year}"

    if not pd.isnull(target_date):
        current_date = pd.Timestamp.now()
        month = current_date.strftime("%B")  # Get the current month name
        year = str(current_date.year)[
            -2:
        ]  # Get the last two digits of the current year
        return f"\\CSE\\CSE Solution Engineering\\{month}'{year}"

    return "\\CSE\\CSE Solution Engineering"


def update_iteration_path(dataframe):
    # Apply the custom function to update the "Iteration Path" column
    dataframe["Iteration Path"] = dataframe.apply(calculate_iteration_path, axis=1)


def update_feature_start_dates(dataframe):
    # Initialize a dictionary to store the earliest Start Date
    #  for each "Feature" section
    feature_start_dates = {}
    feature_title3_dates = {}

    # Initialize variables to keep track of the current "Feature"
    current_feature = None

    # Iterate through the DataFrame
    for index, row in dataframe.iterrows():
        if row["Work Item Type"] == "Feature":
            # If a new "Feature" is encountered, update the current_feature variable
            current_feature = row["Title 3"]
            feature_start_dates[current_feature] = None
        elif row["Work Item Type"] == "User story" and current_feature:
            # If it's a "User story" and we have a current_feature,
            # check and update the Start Date
            if row["Start Date"] and (
                feature_start_dates[current_feature] is None
                or row["Start Date"] < feature_start_dates[current_feature]
            ):
                feature_start_dates[current_feature] = row["Start Date"]
                # Capture the "Title 3" date
                feature_title3_dates[current_feature] = row["Title 3"]
        else:
            # If it's not a "User story" or not within a "Feature"
            #  section, reset the current_feature
            current_feature = None

    # Update the "Start Date" in the corresponding "Feature" rows
    for feature, start_date in feature_start_dates.items():
        dataframe.loc[
            (dataframe["Work Item Type"] == "Feature")
            & (dataframe["Title 3"] == feature),
            "Start Date",
        ] = start_date

    return dataframe


def update_feature_target_dates(dataframe):
    # Initialize a dictionary to store the latest date for each "Feature" section
    feature_latest_dates = {}

    # Initialize variables to keep track of the current "Feature"
    current_feature = None

    # Iterate through the DataFrame
    for index, row in dataframe.iterrows():
        if row["Work Item Type"] == "Feature":
            # If a new "Feature" is encountered, update the current_feature variable
            current_feature = row["Title 3"]
            feature_latest_dates[current_feature] = None
        elif row["Work Item Type"] == "User story" and current_feature:
            # If it's a "User story" and we have a current_feature,
            # check and update the latest date
            resolved_date = pd.to_datetime(row["Resolved Date"], errors="coerce")
            target_date = pd.to_datetime(row["Target Date"], errors="coerce")

            if not pd.isna(resolved_date) and not pd.isna(target_date):
                # Update the latest date for the current "Feature"
                if feature_latest_dates[current_feature] is None:
                    feature_latest_dates[current_feature] = max(
                        resolved_date, target_date
                    )
                else:
                    feature_latest_dates[current_feature] = max(
                        feature_latest_dates[current_feature],
                        resolved_date,
                        target_date,
                    )
            elif not pd.isna(resolved_date):
                # Update the latest date for the current "Feature" with resolved_date
                if feature_latest_dates[current_feature] is None:
                    feature_latest_dates[current_feature] = resolved_date
                else:
                    feature_latest_dates[current_feature] = max(
                        feature_latest_dates[current_feature], resolved_date
                    )
            elif not pd.isna(target_date):
                # Update the latest date for the current "Feature" with target_date
                if feature_latest_dates[current_feature] is None:
                    feature_latest_dates[current_feature] = target_date
                else:
                    feature_latest_dates[current_feature] = max(
                        feature_latest_dates[current_feature], target_date
                    )

    # Update the "Target Date" column in the corresponding "Feature" rows
    for feature, latest_date in feature_latest_dates.items():
        dataframe.loc[
            (dataframe["Work Item Type"] == "Feature")
            & (dataframe["Title 3"] == feature),
            "Target Date",
        ] = latest_date

    return dataframe


# Marge Reoslved and Target date
def copy_resolved_date_to_target_date(dataframe):
    dataframe["Target Date"] = dataframe.apply(
        lambda row: row["Resolved Date"]
        if pd.notna(row["Resolved Date"])
        else row["Target Date"],
        axis=1,
    )


def update_feature_state(dataframe):
    # Initialize a dictionary to store the state of each "Feature" section
    feature_states = {}

    # Initialize variables to keep track of the current "Feature"
    current_feature = None

    # Iterate through the DataFrame
    for index, row in dataframe.iterrows():
        if row["Work Item Type"] == "Feature":
            # If a new "Feature" is encountered, update the current_feature variable
            current_feature = row["Title 3"]
            feature_states[current_feature] = set()  # Use a set to store unique states
        elif row["Work Item Type"] == "User story" and current_feature:
            # If it's a "User story" and we have a current_feature, update the state
            state = row["State"]
            if state:
                feature_states[current_feature].add(state)
        else:
            # If it's not a "User story" or not within a "Feature"
            #  section, reset the current_feature
            current_feature = None

    # Iterate through the "Feature" sections and update their "State" accordingly
    for feature, states in feature_states.items():
        if len(states) == 1 and "Closed" in states:
            dataframe.loc[
                (dataframe["Work Item Type"] == "Feature")
                & (dataframe["Title 3"] == feature),
                "State",
            ] = "Closed"

    return dataframe


def marge_date(dataframe):
    """Copy values from Resolved Date to Target Date without deleting existing values"""
    dataframe["Target Date"] = dataframe.apply(
        lambda row: row["Resolved Date"]
        if pd.notna(row["Resolved Date"])
        else row["Target Date"],
        axis=1,
    )


print(colored("Functions done", "green"))
# endregion


# region transformations

# Path to the csv file generated from Jira
file_path = "docs/Jira2Dataframe.csv"

# Create a Data Frame
df = pd.read_csv(file_path)

# Path to the JSON file containing new rows
jsonfilepath = "standard_rows.json"

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
    "Target Date",
]

new_df = pd.DataFrame(columns=new_columns)

# Copy values from the original DataFrame 'df' to 'new_df'
new_df["Work Item Type"] = df["Issue Type"].apply(
    lambda x: "User story" if x == "Story" else ""
)
new_df["Title 3"] = df.apply(
    lambda row: "["
    + (
        "GTO"
        if row["Project key"] == "ITS"
        else ("GTOMS" if row["Project key"] == "ITSMS" else str(row["Project key"]))
    )
    + "] "
    + str(row["Epic Link Summary"])
    if row["Project key"] in ["ITS", "ITSMS"]
    else "[" + str(row["Project key"]) + "] " + str(row["Project name"]),
    axis=1,
)

new_df["Title 4"] = df["Summary"]
new_df["Assigned To"] = df["Assignee"]
new_df["State"] = "New"
new_df["Iteration Path"] = "\CSE\CSE Solution Engineering"
new_df["Area Path"] = "\AzureCSE\SolutionEngineering"
new_df["Description"] = df["Description"]
new_df["Acceptance Criteria"] = df["Custom field (Acceptance Criteria)"]
new_df["PG Business Value"] = ""
new_df["Value Area"] = "Business"
new_df["Work Category"] = "Maintenance"
new_df["Tags"] = "EE-AIFactory"
new_df["Start Date"] = df["Created"]
new_df["State 2"] = df["Status"]
new_df["End Date"] = df["Resolved"]

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

change_status_backlog(dataframe_later)

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
marge_date(dataframe_feature_state)
# Save the copy to a CSV file
# dataframe_later.to_csv("docs/dataframe_later.csv", index=False)
# dataframe_feature_start_dates.to_csv("docs/feature_start_dates.csv", index=False)
# dataframe_feature_target_dates.to_csv("docs/feature_target_dates.csv", index=False)
dataframe_feature_state.to_csv("docs/Second.csv", index=False)
print(colored("Second.csv done", "yellow"))
# endregion

print(colored("Finished", "blue"))
