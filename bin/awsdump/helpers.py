
import boto3
import json
import sys
from datetime import date, datetime

"""
TODO: exponential backoff
"""

def aws_get_credentials_for_assumed_role(arn, myconfig):
    """ For a given role to assume
            Returns a credentials dict to be used in boto3.client calls"""
    try:
        sts_client = boto3.client('sts', config=myconfig)
    except Exception, e:
        raise Exception("Exception in aws_get_credentials_for_assumed_role boto3_client('sts') for %s: %s" % (arn, str(e)))
    try:
        assumed_role_object=sts_client.assume_role(
            RoleArn=arn,
            RoleSessionName="blah")
    except Exception, e:
        raise Exception("Exception in aws_get_credentials_for_assumed_role sts_client.assume_role for %s: %s" % (arn, str(e)))
    else:
        return assumed_role_object['Credentials']

def aws_list_accounts(list_accounts_role, myconfig):
    """ Enumerate all accounts by assuming the provided role
            Returns a list of account dicts """
    try:
        credentials = aws_get_credentials_for_assumed_role(list_accounts_role, myconfig)
    except Exception, e:
        raise Exception("Exception in aws_list_accounts: %s" % str(e))
    else:
        try:
            client = boto3.client(
                'organizations',
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken'],
                config=myconfig
            )
        except Exception, e:
            raise Exception("Exception in aws_list_accounts: %s" % str(e))
        else:
            save = []
            accounts=client.list_accounts()
            for account in accounts.get('Accounts', []):
                save.append(account)
            while 'NextToken' in accounts:
                accounts = client.list_accounts(NextToken=accounts['NextToken'])
                for account in accounts.get('Accounts', []):
                    save.append(account)
            return save

def json_serial(obj):
    """ Helper function to serialize certain Pythonic types """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def aws_get_assume_role_from_account(account, role_name):
    """ Given an account dict
            Return the arn of the role to assume """
    return "arn:aws:iam::%s:role/%s" % (account['Id'], role_name)

def aws_get_regions_ec2(arn, myconfig):
    """ Given a role to assume, list all ec2 regions 
            Returns a list of regions """
    try:
        credentials = aws_get_credentials_for_assumed_role(arn, myconfig)
    except Exception, e:
        sys.stderr.write("Exception in aws_describe_ec2: %s\n" % str(e))
        return []
    else:
        client = boto3.client(
            'ec2',
            region_name='us-east-1',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
            config=myconfig
        )
        regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
        return regions
 
def aws_describe_ec2(arn, region, myconfig):
    """ Given a role to assume and a region, list all ec2 instances in that region
            Returns a list of instance dicts """
    try:
        credentials = aws_get_credentials_for_assumed_role(arn, myconfig)
    except Exception, e:
        sys.stderr.write("Exception in aws_describe_ec2: %s\n" % str(e))
        return []
    else:
        save = []
        client = boto3.client(
            'ec2',
            region_name=region,
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
            config=myconfig
        )
        response = client.describe_instances()
        for r in response.get('Reservations', []):
            for i in r.get('Instances', []):
                save.append(i)
        while 'NextToken' in response:
            response = client.describe_instances(NextToken=response['NextToken'])
            for r in response.get('Reservations', []):
                for i in r.get('Instances', []):
                    save.append(i)
        return save

