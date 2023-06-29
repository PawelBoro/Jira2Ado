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
python -m Get-JiraRecordsToXLSX
"""

pip install openpyxl

import pandas as pd

from io impot StringIO
from atlassian import Jira
from creds.credentials import email, api_token, jql_request

# Log in to the Jira Cloud using the API Token
jira = Jira(
    url='https://jira-pg-ds.atlassian.net',
    username=email,
    password=api_token,
    cloud=True)

# Collect the all issues from the Jira Cloud to Json
issues = jira.jql(jql_request)

# Collect the all issues from the Jira Cloud to CSV file
file_csv = jira.csv(jql_request)

# Decode the file_csv from byte to string
file_decoded = file_csv.decode()

# Creates a StringIO object named test using the content of the file_decoded string
JiraRecords_objects = StringIO(file_decoded)

# The code reads data from test, assumed to be in CSV format, using pd.read_csv(), and saves it as a pandas DataFrame named outputFile. Then, the DataFrame is exported to an Excel file named 'output.xlsx' using outputFile.to_excel('output.xlsx')
outputFile = pd.read_csv(JiraRecords_objects, sep=",")
outputFile.to_excel('Get-JiraRecordsToXLSX.xlsx')
