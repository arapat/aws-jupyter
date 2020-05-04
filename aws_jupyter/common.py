import boto.ec2
import json
import os
import subprocess
import sys
import yaml


# DEFAULT_AMI = "ami-08cf5e5716f79b01a"  # Jupyter-tmsn, us-east-1
DEFAULT_AMI = "ami-0fc359be23c460554"  # us-west-2
DEFAULT_REGION = "us-west-2"
DEFAULT_TYPE = "m3.xlarge"

def load_config(args, config_path="~/.tmsn_config"):
    def load_credential(config):
        with open(config["credential"]) as f:
            creds = yaml.safe_load(f)
            creds = list(creds.values())[0]
            config["key"] = creds["key_name"]
            config["key_path"] = creds["ssh_key"]
            config["aws_access_key_id"] = creds["access_key_id"]
            config["aws_secret_access_key"] = creds["secret_access_key"]

    # Load configuration
    config_path = os.path.expanduser(config_path)
    config = {}
    if os.path.isfile(config_path):
        with open(config_path) as f:
            config = yaml.safe_load(f)
    # Load arguments
    if "type" not in args or args["type"] is None:
        if "type" in config:
            args["type"] = config["type"]
        else:
            args["type"] = DEFAULT_TYPE
        print("Instance type is not specified. Default instance type set to '{}'".format(args["type"]))
    if "spot" not in args or args["spot"] is None:
        if "spot" in config:
            args["spot"] = config["spot"]
        else:
            args["spot"] = 0.0
    if "ami" not in args or args["ami"] is None:
        if "ami" in config:
            args["ami"] = config["ami"]
        else:
            args["ami"] = DEFAULT_AMI
        print("AMI is not specified. Default AMI set to '{}'".format(args["ami"]))
    if "region" not in args or args["region"] is None:
        if "region" in config:
            args["region"] = config["region"]
        else:
            args["region"] = DEFAULT_REGION
        print("Region is not specified. Default region set to '{}'".format(args["region"]))
    warning = False
    output = ""
    for t in args:
        if args[t] is not None or t not in config:
            config[t] = args[t]
    # Check the credential file
    if "credential" not in config or not config["credential"]:
        print("Warning: Please provide the path to the credential file.")
        config["credential"] = ""
    config["credential"] = os.path.abspath(config["credential"])
    # Load credential
    try:
        load_credential(config)
    except:
        print("Warning: Failed to load credential.")
    # Save the configuration
    with open(config_path, 'w') as f:
        yaml.dump(config, f)
    # Print arguments
    for t in config:
        if config[t] is None and \
                t in ["ami", "aws_access_key_id", "aws_secret_access_key", "credential",
                      "key", "key_path", "region"]:
            output += "{}:\t{} (WARNING)\n".format(t, config[t])
            warning = True
        else:
            output += "{}:\t{}\n".format(t, config[t])
    print()
    print('=' * 3, "Configuration", '=' * 3)
    print(output)
    if warning:
        print('-' * 10)
        print("WARN: Please check the configurations with the (WARNING) suffix above.")
        print('-' * 10)
        print()
    return config


def query_status(args):
    conn = boto.ec2.connect_to_region(
        args["region"],
        aws_access_key_id=args["aws_access_key_id"],
        aws_secret_access_key=args["aws_secret_access_key"])
    instances = conn.get_only_instances(filters={
        "tag:cluster-name": args["name"],
    })
    return [{
        "state": instance.state,
        "ip_address": instance.ip_address,
    } for instance in instances if instance.state in ["pending", "running"]]


def check_connections(instances, args, timeout=2):
    def try_ssh_instance(url):
        command = ("ssh -o StrictHostKeyChecking=no -i {} ubuntu@{} "
                    "\"echo Hello > /dev/null\"").format(args["key_path"], url)
        print(command)
        try:
            t = subprocess.run(command, shell=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return False
        return t.returncode == 0

    print("Checking the network connections...")
    for url in instances:
        if not try_ssh_instance(url):
            print("Error: Cannot SSH to the instance '{}'. ".format(url) +
                  "Try again later, or if you haven't already, run `check` command")
            return False
    return True
