
# encoding = utf-8

import os
import sys
import time
import datetime
import json
import awsdump.helpers

'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''
'''
# For advanced users, if you want to create single instance mod input, uncomment this method.
def use_single_instance_mode():
    return True
'''

def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    opt_role_to_list_accounts = definition.parameters.get('role_to_list_accounts', None)
    opt_role_to_describe_ec2  = definition.parameters.get('role_to_describe_ec2', None)
    pass

def collect_events(helper, ew):
    """Implement your data collection logic here """

    opt_role_to_list_accounts = helper.get_arg('role_to_list_accounts')
    opt_role_to_describe_ec2  = helper.get_arg('role_to_describe_ec2')

    accounts = awsdump.aws_list_accounts(opt_role_to_list_accounts)
    for account in accounts:
        if account['Status'] == 'ACTIVE':
            role = awsdump.aws_get_assume_role_from_account(account, opt_role_to_list_accounts)
            regions = awsdump.aws_get_regions_ec2(role)
            for region in regions:
                instances = awsdump.aws_describe_ec2(role, region)
                for i in instances:
                    i['Region']=region
                    i['Account']=account['Id']
                    data = json.dumps(i, default=json_serial, indent=2, sort_keys=True)
                    event = helper.new_event(data, time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
                    ew.write_event(event)

