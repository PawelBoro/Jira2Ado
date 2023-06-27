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
python -m jira2ado.py
"""
from jira.client import JIRA
from ./.credentials/credentials import email, api_token, server, jql
import pandas as pd
import sqlite3
import xlsxwriter

print("Age:", jql)
print("email:", email)