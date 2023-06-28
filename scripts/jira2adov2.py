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
python -m jira2adov2
"""
# pip install jira
# pip install atlassian-python-api
import jira.client
import pandas as pd
import sqlite3

from atlassian import Jira
from jira.client import JIRA
from creds.credentials import email, api_token, server, jql
# import xlsxwriter


# Authentication
# basic_auth=(email, api_token)
# print(basic_auth)

# Get issues from Jira in JSON format
# jira = JIRA(options={'server': server}, basic_auth=(email, api_token))
# jira_issues = jira.search_issues(jql)

# Another try to log in and Get issues from jql search
jira = Jira(
    url='https://jira-pg-ds.atlassian.net',
    username=email,
    password=api_token,
    cloud=True)

jql_request = 'project = "AI Factory ITS" AND assignee in (61d425a20586a2006949ffee) AND updated >= -4w'
issues = jira.jql(jql_request)
print(issues)
file = jira.csv(jql_request)

file_decoded = file.decode()

import csv

# Assuming 'decoded_data' contains the decoded string

# Specify the output file path
output_file = 'output.csv'

# Split the decoded data into lines
lines = file_decoded.split('\n')

# Write the lines to a CSV file
with open(output_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for line in lines:
        writer.writerow(line.split(','))

# import csv
# file.csv


# jira.projects(included_archived=None)
# jira.get_all_projects(included_archived=None)

import csv

filename = "data.csv"  # Replace with the actual filename

with open(filename, "rb") as file:
    data = file.read().decode("utf-8-sig")  # Decode bytes to string, remove BOM if present

reader = csv.reader(data.splitlines())
header = next(reader)  # Read the header

for row in reader:
    print(row)  # Process each row as needed
