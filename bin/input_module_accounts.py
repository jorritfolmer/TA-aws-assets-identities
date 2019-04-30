
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
    pass

def collect_events(helper, ew):
    """Implement your data collection logic here """

    loglevel = helper.get_log_level()
    helper.set_log_level(loglevel)
    opt_role_to_list_accounts = helper.get_arg('role_to_list_accounts')

    helper.log_info("Starting list-accounts operation")
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
    helper.log_debug("Got %s accounts back" % len(accounts))
    for account in accounts:
        data = json.dumps(account, default=awsdump.helpers.json_serial, indent=2, sort_keys=True)
        event = helper.new_event(data, time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
        ew.write_event(event)
