import boto3
import botocore
import time
import json

# take user input for iam roles to add to config
iam_role_string = input('Enter comma-separated list of IAM roles to add: ')
iam_role_list = iam_role_string.split(",")

# open file in write mode
f = open('config', 'w')

# establish client with root account (default profile)
session = boto3.Session(profile_name="default")
client = session.client('sts')
org = session.client('organizations')

# paginate through all org accounts
paginator = org.get_paginator('list_accounts')
page_iterator = paginator.paginate()

# get accounts ids for active accounts
account_ids = []
for page in page_iterator:
    for account in page['Accounts']:
        if account['Status'] == 'ACTIVE':
            account_ids += {account['Id']}

# write default config entry
f.write("[default]\nregion = eu-west-2\noutput = json\n")

# write iam role entry for each account id in list
for account_id in account_ids:
    for iam_role in iam_role_list:
        if "RO" in iam_role:
            f.write("\n[profile " + account_id + "-RO]")
            f.write("\nrole_arn = arn:aws:iam::" + account_id + ":role/" + iam_role)
            f.write("\nsource_profile = default\n")
        if "Admin" in iam_role:
            f.write("\n[profile " + account_id + "-Admin]")
            f.write("\nrole_arn = arn:aws:iam::" + account_id + ":role/" + iam_role)
            f.write("\nsource_profile = default\n")

print(".aws/config file updated!")
