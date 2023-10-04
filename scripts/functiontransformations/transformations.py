import pandas as pd


def create_new_dataframe(df):
    # Define desired columns for the new DataFrame
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

    # Create a new DataFrame with the specified columns
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
    new_df["Resolved Date"] = df["Status"]
    new_df["End Date"] = df["Resolved"]

    return new_df


# Usage example:
# Call the function with your original DataFrame 'df'
# new_df = create_new_dataframe(df)
