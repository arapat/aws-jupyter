import argparse
import sys
from .common import load_config


def main_set_config():
    parser = argparse.ArgumentParser(
        description="Set aws-jupyter configurations",
        usage="aws-jupyter config <args>",
    )
    parser.add_argument("--region",
                        help="region name")
    parser.add_argument("-t", "--type",
                        help="the type of the instances")
    parser.add_argument("--ami",
                            help="AMI type")
    parser.add_argument("--credential",
                        required=False,
                        help="path to the credential file")
    config = load_config(vars(parser.parse_args(sys.argv[2:])))
    print("Please set following configuration parameters."
            "Type Enter if the default value is correct.")
    print("Region [{}]: ".format(config["region"]), end='')
    s = input()
    if s.strip():
        config["region"] = s.strip()
    print("Instance type [{}]: ".format(config["type"]), end='')
    s = input()
    if s.strip():
        config["type"] = s.strip()
    print("AMI [{}]: ".format(config["ami"]), end='')
    s = input()
    if s.strip():
        config["ami"] = s.strip()
    print("Credential [{}]: ".format(config["credential"]), end='')
    s = input()
    if s.strip():
        config["credential"] = s.strip()
    load_config(config)
