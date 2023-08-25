#!/usr/bin/env python3
"""
Script synopsis.
# :example
scripts/transform_csv.py
"""

import datetime
import json

import pandas as pd


# Defining functions
def add_rows_to_dataframe(dataframe, json_file_path):
    """
    Add rows to a DataFrame from a JSON file.
    Parameters:
        dataframe (pd.DataFrame): The original DataFrame.
        json_file_path (str): The path to the JSON file containing
        data for new rows.
    Returns:
        pd.DataFrame: The updated DataFrame with the new rows added at the top.
    """
    # Read JSON data from the file
    with open(json_file_path, "r") as json_file:
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


def process_dataframe(dataframe):
    new_rows = []
    rows_to_remove = []
    previous_title_3 = None

    for index, row in dataframe.iterrows():
        title_3 = row["Title 3"]

        if title_3 != previous_title_3:
            # Create a new row with the desired values
            new_row = {
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
                "Tags": "Agility",
                "Start Date": "",
                "Resolved Date": "",
            }
            new_rows.append(new_row)

        # Remove the title from the original row
        row["Title 3"] = ""
        rows_to_remove.append(index)

        previous_title_3 = title_3

    # Create a DataFrame from the new_rows list
    new_rows_df = pd.DataFrame(new_rows)

    # Concatenate the new rows to the original DataFrame
    dataframe = pd.concat([dataframe, new_rows_df], ignore_index=True)

    # Remove the rows with empty "Title 3"
    dataframe = dataframe.drop(rows_to_remove)

    return dataframe

    # Create an empty DataFrame to store the new rows
    new_rows_df = pd.DataFrame(columns=dataframe.columns)

    # Get the unique values in the "Title 3" column
    unique_titles = dataframe["Title 3"].unique()

    for title in unique_titles:
        # Find the index of the first occurrence of the title
        first_occurrence_index = dataframe[dataframe["Title 3"] == title].index[0]

        # Create a new row with the desired values
        new_row = {
            "ID": "",
            "Work Item Type": "Feature",
            "Title 1": "Agility via Product Management",
            "Title 2": "",
            "Title 3": title,
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
            "Tags": "Agility",
            "Start Date": "",
            "Resolved Date": "",
        }

        # Concatenate the new row with the empty DataFrame
        new_rows_df = pd.concat(
            [new_rows_df, pd.DataFrame([new_row])], ignore_index=True
        )

        # Add the new row above the first occurrence of the title
        dataframe = pd.concat(
            [
                dataframe.iloc[:first_occurrence_index],
                new_rows_df,
                dataframe.iloc[first_occurrence_index:],
            ],
            ignore_index=True,
        )

    return dataframe


def add_row_above_first_occurrence(dataframe):
    # Create an empty DataFrame to store the new rows
    new_rows = []

    # Get the unique values in the "Title 3" column
    unique_titles = dataframe["Title 3"].unique()

    for title in unique_titles:
        # Find all occurrences of the title
        occurrence_indices = dataframe[dataframe["Title 3"] == title].index

        # Create a new row with the desired values
        new_row = {
            "ID": "",
            "Work Item Type": "Feature",
            "Title 1": "",
            "Title 2": "",
            "Title 3": title,
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

        # Append the new row to the list
        new_rows.append(new_row)

        # Remove all occurrences of the value from the "Title 3" column
        dataframe.loc[occurrence_indices, "Title 3"] = ""

    # Create a DataFrame from the new_rows list
    new_rows_df = pd.DataFrame(new_rows)

    # Concatenate the new rows with the original DataFrame
    dataframe = pd.concat([new_rows_df, dataframe], ignore_index=True)

    return dataframe


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


# Path to the csv file generated from Jira
file_path = "docs/get_multiple_projects_jira_records_to_csv.csv"

# Create a Data Frame
df = pd.read_csv(file_path)
print(df)

# Path to the JSON file containing new rows
json_file_path = "standard_rows.json"

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
new_df["Title 3"] = "[" + df["Project key"] + "] " + df["Project name"]
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

# Filtering the data
filtered_df = delete_rows_with_empty_work_item_type(new_df)

# Call the function to add new rows from the JSON file
newest_df = add_rows_to_dataframe(filtered_df, json_file_path)

# Processing DataFrame
process_df = process_dataframe(newest_df)
new_dataframe = add_row_above_first_occurrence(filtered_df)
create_feature_rows = create_feature_rows(filtered_df)

# Display the updated DataFrame
print(newest_df)

# Save 'new_df' to a CSV file
newest_df.to_csv("docs/newest_df.csv", index=False)
process_df.to_csv("docs/process_df.csv", index=False)
new_dataframe.to_csv("docs/new_dataframe.csv", index=False)
filtered_df.to_csv("docs/filtered_df.csv", index=False)
create_feature_rows.to_csv("docs/create_feature_rows.csv", index=False)
