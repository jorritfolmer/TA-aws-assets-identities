# AWS asset and identity technical add-on for Splunk

## What does this add-on do?

1. It enumerates all accounts from an AWS Organizations master account
2. It describes the following resources in every AWS region and in every account previously found:
   * EC2 instances
   * S3 buckets and their policy
   * (more to come)

## Why does this add-on exist?

To plug the information gap between CMDB's and reality in a structural way. CMDB's are rarely up-to-date and acurate because they aren't the primary source of truth. The best place to query asset reality is through primary sources like platform API's.

This add-on only needs two parameters to reach an acurate 99% picture of cloud assets. Doing this with the Splunk AWS add-on involves a lot of manual work. It also involves eternal vigilance because new accounts aren't automatically included. This add-on fixes that.

## But I want 100% coverage!

You can, by enriching the data from this add-on with information about short living instances through Cloudtrail logging of API requests (RunInstances or StartInstances). 

## How do I use this add-on?

Install this add-on on a Splunk Enterprise instance, heavy forwarder style.

### Dump all AWS accounts in an AWS organization

Create a new "Accounts" input:
   * Give the input a name, e.g. "All_Accounts"
   * Specify an interval for data collection, e.g. 86400 for daily
   * Specify a Splunk index to dump the information in
   * Specify a role within the AWS master account to assume, and is allowed to perform ListAccounts (e.g. arn:aws:iam::123456789:role/tf-list-accounts-role

Note: you do not need this input for other inputs to work. Only use this input if you're interested in account information for futher correlation within Splunk searches

### Dump all EC2 instances in all regions within all accounts

Create a new "EC2" input: 
   * Give the input a name, e.g. "All_EC2"
   * Specify an interval for data collection, e.g. 86400 for daily
   * Specify a Splunk index to dump the information in
   * Specify a role within the AWS master account to assume, and is allowed to perform ListAccounts (e.g. arn:aws:iam::123456789:role/tf-list-accounts-role
   * Specify the last constant part of the arn in every account that is allowed to perform DescibeInstances (e.g. tf-ec2-describe-role)

This requires some setup up front by your friendly AWS administrator. Every account, and every new account should contain a role that this input is allowed to assume, and is allowed to perform DescribeInstances. Since you're in AWS, this should probably be automated ad fundum anyway.


