#!/usr/bin/env python
import argparse
import os
import sys

from operator import itemgetter
from .common import load_config
from .common import query_status


def ssh_headnode(args):
    args = load_config(args)
    all_status = query_status(args)
    if len(all_status) == 0:
        print("No instance found in the cluster '{}'. Quit.".format(args["name"]))
        return

    ready_ip_address = [t["ip_address"] for t in all_status if t["state"] == "running"]
    if len(ready_ip_address) == 0:
        print("No instance is ready. Quit.")
    else:
        print("Connecting to the first node.")
        os.system("ssh -i {} ubuntu@{}".format(args["key_path"], ready_ip_address[0]))


def main_ssh_headnode():
    parser = argparse.ArgumentParser(
        description="SSH into the head node of a cluster",
        usage="aws-jupyter config <args>",
    )
    parser.add_argument("--name",
                        required=False,
                        help="cluster name")
    parser.add_argument("--region",
                        help="Region name")
    parser.add_argument("--credential",
                        help="path to the credential file")
    args = vars(parser.parse_args(sys.argv[2:]))
    ssh_headnode(args)


if __name__ == '__main__':
    main_ssh_headnode()
