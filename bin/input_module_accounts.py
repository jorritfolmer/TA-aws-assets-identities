
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
    pass

def collect_events(helper, ew):
    """Implement your data collection logic here """

    loglevel = helper.get_log_level()
    helper.set_log_level(loglevel)
    proxy = helper.get_proxy()
    opt_role_to_list_accounts = helper.get_arg('role_to_list_accounts')

    helper.log_info("Starting list-accounts operation")
    if proxy.get('proxy_url', False):
        helper.log_debug(proxy)
        os.environ["HTTP_PROXY"] = "http://%s:%s" % (proxy['proxy_url'], proxy['proxy_port'])
        os.environ["HTTPS_PROXY"] = "http://%s:%s" % (proxy['proxy_url'], proxy['proxy_port'])
        os.environ["NO_PROXY"] = "169.254.169.254"
    accounts = awsdump.helpers.aws_list_accounts(opt_role_to_list_accounts)
    helper.log_debug("Got %s accounts back" % len(accounts))
    for account in accounts:
        data = json.dumps(account, default=awsdump.helpers.json_serial, indent=2, sort_keys=True)
        event = helper.new_event(data, time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
        ew.write_event(event)
