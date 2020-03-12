import argparse
import sys
from .common import load_config

from .common import DEFAULT_AMI
from .common import DEFAULT_REGION


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
    parser.add_argument("--default-ami",
                        action="store_true",
                        help="use default ami")
    parser.add_argument("--default-region",
                        action="store_true",
                        help="use default region {}".format(DEFAULT_REGION))

    user_configs = vars(parser.parse_args(sys.argv[2:]))
    if user_configs["default_ami"]:
        if user_configs["ami"] is not None:
            print("Error: The arguments '--default-ami' and '--ami' cannot be both set.")
            sys.exit(1)
        user_configs["ami"] = DEFAULT_AMI
    if user_configs["default_region"]:
        if user_configs["region"] is not None:
            print("Error: The arguments '--default-region' and '--region' cannot be both set.")
            sys.exit(1)
        user_configs["region"] = DEFAULT_REGION
    config = load_config(user_configs)
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
