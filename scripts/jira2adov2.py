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
import csv
from atlassian import Jira
# from jira.client import JIRA
from creds.credentials import email, api_token

# Another try to log in and Get issues from jql search
jira = Jira(
    url='https://jira-pg-ds.atlassian.net',
    username=email,
    password=api_token,
    cloud=True)

jql_request = 'project = "AIF ITS Microsoft" AND assignee in (61d425a20586a2006949ffee, 5dde91bb7eb2280d03c98dd0, 63c927cee28ec74364cc8f59, 6405ed610e0ddcdce18e3980, 62c7ec27b6357aecd7c7e693) AND updated >= -4w'
issues = jira.jql(jql_request)
print(issues)

file_csv = jira.csv(jql_request)

file_decoded = file_csv.decode()

# Specify the output file path
output_file = 'output3.csv'

# Split the decoded data into lines
lines = file_decoded.split('\n')

# Write the lines to a CSV file
with open(output_file, mode='w') as file:
    writer = csv.writer(file)
    for line in lines:
        writer.writerow(line.split(','))

output_file = 'output4.csv'
lines = file_decoded.split('\n')

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    for line in lines:
        values = line.split(',')
        if values:
            writer.writerow(values)
        else:
            print(f"Skipping line: {line}")
