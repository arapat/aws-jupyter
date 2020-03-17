#!/usr/bin/env python
import argparse
import boto.ec2
from boto.exception import EC2ResponseError

from .common import load_config
from .common import query_status
from .create_cluster import SECURITY_GROUP_NAME


def check_access(args):
    conn = boto.ec2.connect_to_region(
        args["region"],
        aws_access_key_id=args["aws_access_key_id"],
        aws_secret_access_key=args["aws_secret_access_key"],
    )
    try:
        default_vpc = conn.describe_account_attributes("default-vpc")[0].attribute_values[0]
        print("Default VPC: {}.\nYour access credentials are valid.".format(default_vpc))
    except EC2ResponseError as e:
        print("Access credentials are invalid: {}".format(e.reason))
        print("aws_access_key_id={}".format(args["aws_access_key_id"]))
        print("aws_secret_access_key={}".format(args["aws_secret_access_key"]))
        return False
    return True


def main_check_access():
    argparse.ArgumentParser(description="Check if the access credentials of AWS is valid")
    config = load_config({})
    return check_access(config)


if __name__ == '__main__':
    main_check_access()