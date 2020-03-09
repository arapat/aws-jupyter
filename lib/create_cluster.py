#!/usr/bin/env python
import boto.ec2
import argparse
import subprocess
import sys
import json

from lib.common import load_config
from lib.common import query_status
from lib.common import DEFAULT_AMI


DEFAULT_TYPE = "m3.xlarge"


def create_default_security_group(conn):
    '''
    Create a default security group
    '''
    security_group_name = "aws-jupyter"

    # Delete the default security group if it exists
    for sg in conn.get_all_security_groups():
        if sg.name == security_group_name:
            try:
                sg.delete()
                break
            except:
                pass
    # Create the new deafult security group
    try:
        sg = conn.create_security_group(security_group_name, "for " + security_group_name)
        sg.authorize("tcp", 0, 65535, "0.0.0.0/0")
    except:
        print(f"Warning: creating a new security group '{security_group_name}' failed")


def create_cluster(args):
    conn = boto.ec2.connect_to_region(
        args["region"],
        aws_access_key_id=args["aws_access_key_id"],
        aws_secret_access_key=args["aws_secret_access_key"])
    create_default_security_group(conn)
    all_status = query_status(args)
    if len(all_status):
        print("Error: A cluster with the name '{}' exists. ".format(args["name"]) +
              "Please choose a different cluster name.\n" +
              "Note: If you want to check the status of the cluster '{}', ".format(args["name"]) +
              "please use `./aws-jupyter.py check` or `./check-cluster.py`.")
        return

    # TODO: removed "--associate-public-ip-address" from the options, check if things still work
    print("Creating the cluster...")
    if args["ondemand"]:
        print("We will use spot instances.")
        reservation = conn.request_spot_instances(
            price=3.0,
            image_id=args["ami"],
            count=args["count"],
            type='one-time',
            key_name=args["key"],
            security_groups=["aws-jupyter"],
            instance_type=args["type"],
            dry_run=False)
    else:
        print("We will use on-demand instances.")
        reservation = conn.run_instances(
            args["ami"],
            min_count=args["count"],
            max_count=args["count"],
            key_name=args["key"],
            security_groups=["aws-jupyter"],
            instance_type=args["type"],
            dry_run=False)
    print("Launched instances:")
    for instance in reservation.instances:
        instance.add_tag("cluster-name", args["name"])
        if args["ondemand"]:
            print("{} (on demand)".format(instance.id))
        else:
            print("{} ({})".format(instance.id, instance.state))
    print("\nDone.")


def main_create_cluster():
    parser = argparse.ArgumentParser(
        description="Crate a cluster using AWS spot instances",
        usage="aws-jupyter.py create [<args>]",
    )
    parser.add_argument("-c", "--count",
                        required=True,
                        help="the number of instances in the cluster")
    parser.add_argument("--name",
                        required=False,
                        default="aws-jupyter-default",
                        help="cluster name")
    parser.add_argument("-t", "--type",
                        help="the type of the instances")
    parser.add_argument("--region",
                        help="Region name")
    parser.add_argument("--ami",
                         help="AMI type")
    parser.add_argument("--credential",
                        help="path to the credential file")
    args = vars(parser.parse_args(sys.argv[2:]))
    if args["ami"] is None:
        print("AMI is not specified. Default AMI set to '{}'".format(DEFAULT_AMI))
        args["ami"] = DEFAULT_AMI
    if args["type"] is None:
        print("Instance type is not specified. Default instance type set to '{}'".format(
            DEFAULT_TYPE))
        args["type"] = DEFAULT_TYPE
    config = load_config(args)
    create_cluster(config)


if __name__ == '__main__':
    main_create_cluster()