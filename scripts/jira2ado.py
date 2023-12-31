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
python -m jira2ado
"""
pip install jira
pip install atlassian-python-api
import jira.client
import pandas as pd
import sqlite3

from atlassian import Jira
from jira.client import JIRA
from creds.credentials import email, api_token, server, jql
# import xlsxwriter


# Authentication
basic_auth=(email, api_token)
print(basic_auth)

# Get issues from Jira in JSON format
jira = JIRA(options={'server': server}, basic_auth=(email, api_token))
jira_issues = jira.search_issues(jql)

#Another try to log in and Get issues from jql search
jira = Jira(
    url='https://jira-pg-ds.atlassian.net',
    username=email,
    password=api_token,
    cloud=True)

jql_request = 'project = "AI Factory ITS" AND assignee in (61d425a20586a2006949ffee) AND updated >= -4w'
issues = jira.jql(jql_request)
print(issues)
file = jira.csv(jql_request)

import csv
file.csv


jira.projects(included_archived=None)
jira.get_all_projects(included_archived=None)