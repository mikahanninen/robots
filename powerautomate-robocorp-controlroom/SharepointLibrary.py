import json
import re

regex = r".*ITEMBODYSTART(.*)ITEMBODYEND.*"

def get_sharepoint_issue_from_email_body(email_body):
    match = re.match(regex, email_body)
    issue = {}
    if match:
        issue = json.loads(match.group(1))
    return issue
