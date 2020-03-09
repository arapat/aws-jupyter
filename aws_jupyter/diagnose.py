#!/usr/bin/env python
import argparse
import subprocess
import sys

from .common import load_config
from .common import query_status
from .create_cluster import SECURITY_GROUP_NAME


def diagnose(args):
    check_security_group = """
    AWS_ACCESS_KEY_ID="{}" AWS_SECRET_ACCESS_KEY="{}" \
    aws ec2 describe-security-groups --region {} --group-names {}
    """.format(
        args["aws_access_key_id"],
        args["aws_secret_access_key"],
        args["region"],
        SECURITY_GROUP_NAME,
    )
    print("Checking security group...")
    subprocess.run(check_security_group, shell=True, check=True)


def main_diagnose():
    parser = argparse.ArgumentParser(description="Print diagnose info on an exsting cluster")
    parser.add_argument("--name",
                        help="cluster name")
    parser.add_argument("--credential",
                        help="path to the credential file")
    parser.add_argument("--region",
                        help="Region name")
    args = vars(parser.parse_args(sys.argv[2:]))
    config = load_config(args)
    diagnose(config)


if __name__ == '__main__':
    main_diagnose()