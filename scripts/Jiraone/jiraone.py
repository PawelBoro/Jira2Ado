from jiraone import LOGIN, issue_export
import json

file = "config.json"
config = json.load(open(file))
LOGIN(**config)

jql = 'project = "AIF ITS Microsoft" AND assignee in (61d425a20586a2006949ffee, 5dde91bb7eb2280d03c98dd0, 63c927cee28ec74364cc8f59, 6405ed610e0ddcdce18e3980, 62c7ec27b6357aecd7c7e693) AND updated >= -4w'
issue_export(jql=jql)