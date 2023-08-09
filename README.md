# auto-update-aws-config
Automatically updates your local AWS config file with the current AWS organisations account data, based on user-specified IAM roles to create AWS profiles.

## Installation
Simply copy the python script to your local directory and execute! This script will attempt to modify your ~/.aws/config file. If you are a windows user or your AWS config file is located elsewhere, please update this static reference (line 9) accordingly.

```bash
python3 auto-update-config.py
```

## User Inputs
The script will prompt you for any IAM roles that you would like to access via a designated profile. Currently the script will create distinct profiles per account id IF the IAM role(s) contain 'RO' or 'Admin' substrings.

For instance, the below entry will create two profiles per account id:

```bash
Enter comma-separated list of IAM roles to add: CCS_Security_RO,CCS_Security_Admin
```

Distinct profiles will be created, even if the IAM role(s) specified don't apply to ALL the account ids listed within an aws organisation:

```python
[default]
region = eu-west-2
output = json

[profile 111111111111-RO]
role_arn = arn:aws:iam::111111111111:role/CCS_Security_RO
source_profile = default

[profile 111111111111-Admin]
role_arn = arn:aws:iam::111111111111:role/CCS_Security_Admin
source_profile = default
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[GNU GPLv3]
(https://choosealicense.com/licenses/gpl-3.0/)