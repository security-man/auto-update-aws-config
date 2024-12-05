import csv
import boto3
import os

# take user input for iam roles to add to config
iam_role_string = input('Enter comma-separated list of IAM roles to add: ')
iam_role_list = iam_role_string.split(",")

# open file in write mode
f = open(os.path.expanduser('~/.aws/config'), 'w')

# open csv file in write mode (for hyperlinking roles)
f_csv = open(os.path.expanduser('aws_accounts.csv'),'w',newline='')
csv_fieldnames = ['Name','AccountID','Role']
csv_writer = csv.DictWriter(f_csv,fieldnames=csv_fieldnames)
csv_writer.writeheader()

# establish client with root account (default profile)
session = boto3.Session(profile_name="default")
client = session.client('sts')
org = session.client('organizations')

# paginate through all org accounts
paginator = org.get_paginator('list_accounts')
page_iterator = paginator.paginate()

# get accounts ids for active accounts
account_ids = []
account_names = []
account_name_sanitised = ""
for page in page_iterator:
	for account in page['Accounts']:
		if account['Status'] == 'ACTIVE':
			account_ids += {account['Id']}
			account_name_sanitised = account['Name']
			account_name_sanitised = ''.join(account_name_sanitised.split())
			account_names += {account_name_sanitised}

# write default config entry
f.write("[default]\nregion = eu-west-2\noutput = json\n")

# write iam role entry for each account id in list
i = 0
for account_id in account_ids:
	for iam_role in iam_role_list:
		if "RO" in iam_role:
			f.write("\n[profile " + account_id + "-RO]")
			f.write("\nrole_arn = arn:aws:iam::" + account_id + ":role/" + iam_role)
			f.write("\nsource_profile = default")
			f.write("\nrole_session_name = " + account_names[i] + "\n")
			csv_writer.writerow({'Name': account_names[i],'AccountID': account_id,'Role': "=HYPERLINK(\"https://signin.aws.amazon.com/switchrole?roleName=" + iam_role + "&account=" + account_id + "&displayName=" + account_names[i] + "\",\"" + iam_role + "\")"})
		if "Admin" in iam_role:
			f.write("\n[profile " + account_id + "-Admin]")
			f.write("\nrole_arn = arn:aws:iam::" + account_id + ":role/" + iam_role)
			f.write("\nsource_profile = default")
			f.write("\nrole_session_name = " + account_names[i] + "\n")
			csv_writer.writerow({'Name': account_names[i],'AccountID': account_id,'Role': "=HYPERLINK(\"https://signin.aws.amazon.com/switchrole?roleName=" + iam_role + "&account=" + account_id + "&displayName=" + account_names[i] + "\",\"" + iam_role + "\")"})

	i += 1

f.close()
f_csv.close()
print(".aws/config file updated!")
