
# encoding = utf-8

import os
import sys
import time
import datetime
import json
import awsdump.helpers
from botocore.config import Config

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

    loglevel = helper.get_log_level()
    helper.set_log_level(loglevel)
    proxy = helper.get_proxy()
    opt_role_to_list_accounts = helper.get_arg('role_to_list_accounts')
    opt_role_to_describe_ec2  = helper.get_arg('role_to_describe_ec2')

    helper.log_info("Starting operation")

    proxy = helper.get_proxy()
    proxies = {}
    if proxy.get('proxy_url', False):
        if(proxy["proxy_username"] and proxy["proxy_password"]):
            proxy_url = "%s://%s:%s@%s:%s" % (proxy["proxy_type"], proxy["proxy_username"], proxy["proxy_password"], proxy["proxy_url"], proxy["proxy_port"])
            proxies = {
                "http" : proxy_url,
                "https" : proxy_url
            }
        else:
            proxy_url = "%s://%s:%s" % (proxy["proxy_type"], proxy["proxy_url"], proxy["proxy_port"])
            proxies = {
                "http" : proxy_url,
                "https" : proxy_url
            }
    myconfig = Config(proxies=proxies)

    accounts = awsdump.helpers.aws_list_accounts(opt_role_to_list_accounts, myconfig)
    for account in accounts:
        if account['Status'] == 'ACTIVE':
            helper.log_debug("Starting ec2 describe for account %s" %account['Id'])
            role = awsdump.helpers.aws_get_assume_role_from_account(account, opt_role_to_describe_ec2)
            regions = awsdump.helpers.aws_get_regions_ec2(role, myconfig)
            for region in regions:
                helper.log_debug("Starting ec2 describe for account %s in region %s" % (account['Id'], region))
                instances = awsdump.helpers.aws_describe_ec2(role, region, myconfig)
                helper.log_debug("Got %d ec2 instances for account %s in region %s" % (len(instances), account['Id'], region))
                for i in instances:
                    i['Region']=region
                    i['Account']=account['Id']
                    data = json.dumps(i, default=awsdump.helpers.json_serial, indent=2, sort_keys=True)
                    event = helper.new_event(data, time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
                    ew.write_event(event)

    helper.log_info("Ended operation")
