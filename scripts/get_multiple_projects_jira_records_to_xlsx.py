"""
# Atlassian Python API
https://community.atlassian.com/t5/Marketplace-Apps-Integrations/Python-APIs-for-Atlassian-Jira-Software/ba-p/1907722
https://atlassian-python-api.readthedocs.io/
https://jira.readthedocs.io/installation.html
https://jira.readthedocs.io/examples.html

# Other
https://whoek.com/b/use-jira-api-to-create-excel-reports.html
https://community.atlassian.com/t5/Jira-questions/Fetch-Jira-details-in-excel-using-python/qaq-p/763401
https://stackoverflow.com/questions/49614493/feth-jira-details-in-excel-using-python
https://community.atlassian.com/t5/Jira-questions/Importing-issues-from-JIRA-to-Excel-using-API/qaq-p/1943319

conda activate jta
python -m get_multiple_projects_jira_records_to_xlsx
"""
from io import StringIO

import pandas as pd
from atlassian import Jira
from creds.credentials import api_token, email, project_names

# Log in to the Jira Cloud using the API Token
jira = Jira(
    url="https://jira-pg-ds.atlassian.net",
    username=email,
    password=api_token,
    cloud=True,
)

# Create an empty DataFrame to store the combined data
combined_data = pd.DataFrame()

# Iterate over each project name
for project_name in project_names:
    jql_request = (
        f'project = "{project_name}" AND assignee in '
        "(61d425a20586a2006949ffee, 5dde91bb7eb2280d03c98dd0, 63c927cee28ec74364cc8f59,"
        " 6405ed610e0ddcdce18e3980, 62c7ec27b6357aecd7c7e693) AND updated >= -4w"
    )

    # Collect all issues from the Jira Cloud to Json
    issues = jira.jql(jql_request)

    # Collect all issues from the Jira Cloud to CSV file
    file_csv = jira.csv(jql_request)

    # Check if file_csv is empty
    if not file_csv:
        print(f"No data for project '{project_name}'. Skipping...")
        continue

    # Decode the file_csv from byte to string
    file_decoded = file_csv.decode()

    # Create a StringIO object using the content of the file_decoded string
    jira_records = StringIO(file_decoded)

    # Read data from jira_records, assumed to be in CSV format,
    # and save it as pandas DataFrame
    jira_data = pd.read_csv(jira_records, sep=",")

    # Append the jira_data to the combined_data DataFrame
    combined_data = combined_data.append(jira_data)

# Save the combined_data to an Excel file named 'Get-JiraRecordsToXLSX.xlsx'
combined_data.to_excel("get_multiple_projects_jira_records_to_xlsx.xlsx", index=False)
