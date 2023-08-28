#!/usr/bin/env python3
"""
Script synopsis.
# :example
scripts/transform_csv.py
"""

import json

import pandas as pd


# Defining functions
def add_rows_to_dataframe(dataframe, jsonfilepath):
    # Read JSON data from the file
    with open(jsonfilepath, "r") as json_file:
        json_data = json.load(json_file)

    # Create a new DataFrame with the specified JSON data
    new_rows = pd.DataFrame(json_data)

    # Concatenate the new rows at the top of the original DataFrame
    dataframe = pd.concat([new_rows, dataframe], ignore_index=True)

    return dataframe


def delete_rows_with_empty_work_item_type(dataframe):
    """
    Delete rows where the 'Work Item Type' column is empty.

    Parameters:
        dataframe (pd.DataFrame): The DataFrame to modify.

    Returns:
        pd.DataFrame: The DataFrame with empty 'Work Item Type' rows removed.
    """
    # Use boolean indexing to filter rows where 'Work Item Type' is not empty
    filtered_dataframe = dataframe[dataframe["Work Item Type"] == "User story"]

    return filtered_dataframe


def create_feature_rows(dataframe):
    # Create an empty DataFrame to store the new rows
    new_rows_df = pd.DataFrame(columns=dataframe.columns)

    # Initialize the current_title variable
    current_title = None

    for index, row in dataframe.iterrows():
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
                "State": "Active",
                "Iteration Path": "\\Cloud General Sprints",
                "Area Path": "\\AzureCSE\\SolutionEngineering",
                "Description": "",
                "Acceptance Criteria": "",
                "PG Business Value": "AI Factory Project delivery",
                "Value Area": "Business",
                "Work Category": "",
                "Tags": "EE-ProductEnhancement",
                "Start Date": "",
                "Resolved Date": "",
            }
            new_rows_df = new_rows_df.append(new_feature_row, ignore_index=True)

            # Update the current_title
            current_title = title_3

        # Append the original row
        new_rows_df = new_rows_df.append(row, ignore_index=True)

    return new_rows_df


def delete_title3_for_user_stories(dataframe):
    # Delete the value from "Title 3" for "User story" rows
    for index, row in dataframe.iterrows():
        if row["Work Item Type"] == "User story":
            dataframe.at[index, "Title 3"] = ""
    return dataframe


def change_names(dataframe):
    # Define a mapping of name changes
    name_mapping = {
        "Pawel Borowiak": "Borowiak, Pawel",
        "kamil gajek": "Kamil Gajek",
        "maciej znalezniak": "Maciej Znalezniak",
    }

    # Apply the name changes to the "Assigned To" column
    dataframe["Assigned To"] = (
        dataframe["Assigned To"].map(name_mapping).fillna(dataframe["Assigned To"])
    )

    # Return the updated DataFrame
    return dataframe


# Path to the csv file generated from Jira
file_path = "docs/get_multiple_projects_jira_records_to_csv.csv"

# Create a Data Frame
df = pd.read_csv(file_path)
print(df)

# Path to the JSON file containing new rows
jsonfilepath = "standard_rows.json"

# Get the current date
current_date = pd.Timestamp.now()

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

# Copy values from the original DataFrame 'df' to 'new_df'
new_df["Work Item Type"] = df["Issue Type"].apply(
    lambda x: "User story" if x == "Story" else ""
)
new_df["Title 3"] = df.apply(
    lambda row: "[" + str(row["Project key"]) + "] " + str(row["Epic Link Summary"])
    if row["Project key"] in ["ITS", "ITSMS"]
    else "[" + str(row["Project key"]) + "] " + str(row["Project name"]),
    axis=1,
)
new_df["Title 4"] = df["Summary"]
new_df["Assigned To"] = df["Assignee"]
new_df["State"] = "New"
new_df["Iteration Path"] = "\Cloud General Sprints"
new_df["Area Path"] = "\AzureCSE\SolutionEngineering"
new_df["Description"] = df["Description"]
new_df["Acceptance Criteria"] = df["Custom field (Acceptance Criteria)"]
new_df["PG Business Value"] = ""
new_df["Value Area"] = "Business"
new_df["Work Category"] = "Business Request"
new_df["Tags"] = "EE-ProductEnhancement"
new_df["Start Date"] = df["Created"]
new_df["Resolved Date"] = current_date + pd.DateOffset(months=3)

# Sort 'new_df' by the 'Title 3' column
new_df.sort_values(by="Title 3", inplace=True)

# Reset the index if needed
new_df.reset_index(drop=True, inplace=True)

# Filtering the data
filtered_df = delete_rows_with_empty_work_item_type(new_df)

# Processing DataFrame
create_fea_rows = create_feature_rows(filtered_df)
delete_df = delete_title3_for_user_stories(create_fea_rows)

# Call the function to add new rows from the JSON file
newest_df = add_rows_to_dataframe(create_fea_rows, jsonfilepath)

# Change the names for ADO
new_names_df = change_names(newest_df)

# Display the updated DataFrame
print(newest_df)

# Save 'new_df' to a CSV file
newest_df.to_csv("docs/newest_df.csv", index=False)
delete_df.to_csv("docs/delete_df.csv", index=False)
filtered_df.to_csv("docs/filtered_df.csv", index=False)
create_fea_rows.to_csv("docs/create_feature_rows.csv", index=False)
