#!/usr/bin/env python
import boto.ec2
import argparse
import subprocess
import sys
import json
from time import sleep
from boto.ec2.blockdevicemapping import BlockDeviceType
from boto.ec2.blockdevicemapping import BlockDeviceMapping
from boto.exception import EC2ResponseError

from .common import load_config
from .common import query_status
from .common import DEFAULT_AMI
from .common import DEFAULT_REGION


DEFAULT_TYPE = "m3.xlarge"
SECURITY_GROUP_NAME = "aws-jupyter"


def create_default_security_group(conn):
    '''
    Create a default security group
    '''
    # Delete the default security group if it exists
    for sg in conn.get_all_security_groups():
        if sg.name == SECURITY_GROUP_NAME:
            try:
                sg.delete()
                break
            except:
                pass
    # Create the new deafult security group
    try:
        sg = conn.create_security_group(SECURITY_GROUP_NAME, "for " + SECURITY_GROUP_NAME)
        sg.authorize("tcp", 0, 65535, "0.0.0.0/0")
    except:
        print(f"Warning: creating a new security group '{SECURITY_GROUP_NAME}' failed")


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
              "please use `aws-jupyter check`.")
        return

    # TODO: removed "--associate-public-ip-address" from the options, check if things still work
    print("Creating the cluster...")
    # Declare the block device mapping for ephemeral disks
    # TODO: adjust mount points, read this: https://cloudinit.readthedocs.io/en/latest/topics/examples.html#adjust-mount-points-mounted
    device_mapping = BlockDeviceMapping()
    for i in range(24):
        eph = BlockDeviceType()
        eph.ephemeral_name = 'ephemeral%d' % i
        device_mapping['/dev/sd{}'.format(chr(ord('b') + i))] = eph
    if args["spot"] > 0.0:
        print("We will use spot instances.")
        try:
            reservation = conn.request_spot_instances(
                price=float(args["spot"]),
                placement=f"{args['region']}c",
                image_id=args["ami"],
                count=args["count"],
                type='one-time',
                key_name=args["key"],
                security_groups=[SECURITY_GROUP_NAME],
                instance_type=args["type"],
                block_device_map=device_mapping,
                dry_run=False)
        except EC2ResponseError as e:
            err_msg = e.message
            print("Error: " + err_msg)
            if "image id" in err_msg.lower():
                print("If you are using the default AMI, try upgrade aws-jupyter " +
                "by `pip install --upgrade aws-jupyter`.")
            sys.exit(1)
        request_ids = [r.id for r in reservation]
        print("Please wait till the spot instances are fullfilled", end='')
        i = 0
        instance_ids = []
        while i < len(request_ids):
            request_id = request_ids[i]
            try:
                spot_req = conn.get_all_spot_instance_requests(request_ids=[request_id])[0]
            except EC2ResponseError:
                print(";", end='')
                sleep(2)
                continue
            if spot_req.state == 'failed':
                print("\nError: Spot request failed")
                # TODO: cancel the spot request
                sys.exit(1)
            if not spot_req.instance_id:
                print(".", end='')
                sleep(2)
                continue
            instance_ids.append(spot_req.instance_id)
            i += 1
        print()
    else:
        print("We will use on-demand instances.")
        try:
            reservation = conn.run_instances(
                args["ami"],
                min_count=args["count"],
                max_count=args["count"],
                key_name=args["key"],
                security_groups=[SECURITY_GROUP_NAME],
                instance_type=args["type"],
                block_device_map=device_mapping,
                dry_run=False)
        except EC2ResponseError as e:
            err_msg = e.message
            print("Error: " + err_msg)
            if "image id" in err_msg.lower():
                print("If you are using the default AMI, try upgrade aws-jupyter " +
                "by `pip install --upgrade aws-jupyter`.")
            sys.exit(1)
        instance_ids = [instance.id for instance in reservation.instances]
    print("Setting tags.")
    conn.create_tags(instance_ids, {"cluster-name": args["name"]})
    print("Launched instances:")
    for instance in instance_ids:
        if args["spot"] > 0.0:
            print("{} (spot)".format(instance))
        else:
            print("{} (on demand)".format(instance))
    print("Done.")


def main_create_cluster():
    parser = argparse.ArgumentParser(
        description="Crate a cluster using AWS spot instances",
        usage="aws-jupyter create [<args>]",
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
    parser.add_argument("--spot",
                        help="the max price for spot instances, if not set, \
                        will use on-demand instances",
                        type=float)
    args = vars(parser.parse_args(sys.argv[2:]))
    if args["ami"] is None:
        print("AMI is not specified. Default AMI set to '{}'".format(DEFAULT_AMI))
        args["ami"] = DEFAULT_AMI
    if args["type"] is None:
        print("Instance type is not specified. Default instance type set to '{}'".format(
            DEFAULT_TYPE))
        args["type"] = DEFAULT_TYPE
    if args["spot"] is None:
        args["spot"] = 0.0
    config = load_config(args)
    if args["region"] != DEFAULT_REGION:
        print("We only support {} region. Please change the configuration by running \
                `aws-jupyter config`.".format(DEFAULT_REGION))
    else:
        create_cluster(config)


if __name__ == '__main__':
    main_create_cluster()