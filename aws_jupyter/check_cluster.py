#!/usr/bin/env python
import argparse
import sys
import os
import aws_jupyter

from operator import itemgetter
from .common import load_config
from .common import query_status
from .run_cluster import run_cluster


def check_cluster(args):
    print("Checking the cluster '{}'...".format(args["name"]))
    all_status = query_status(args)
    if len(all_status) == 0:
        print("No instance found in the cluster '{}'. Quit.".format(args["name"]))
        return

    cluster_status = None
    total = len(all_status)
    ready = len([t for t in all_status if t["state"] == "running"])
    cluster_status = (ready, total)
    neighbors = list(map(lambda t: t["ip_address"], all_status))
    print("    Total instances: {}\n    Running: {}".format(total, ready))
    if ready == 0:
        print("    Instances status: {}".format(all_status[0]["state"]))
    if total > 0:
        with open("neighbors.txt", 'w') as f:
            if total == ready:
                f.write("Ready. ")
            else:
                f.write("NOT ready. ")
            f.write("IP addresses of all instances:\n")
            f.write('\n'.join(neighbors))
        print("    The public IP addresses of the instances have been written into "
              "`./neighbors.txt`")
    return cluster_status


def check_status_and_init(args):
    args = load_config(args)
    status = check_cluster(args)
    ready, total = 0, 0
    if status is not None:
        ready, total = status
    if ready > 0 and ready == total:
        print("Cluster is running (yet might still being initialized). \
                I will try to start Jupyter notebook now.")
        script_dir = os.path.join(os.path.dirname(aws_jupyter.__file__), "scripts")
        args["files"] = ["./neighbors.txt"]
        args["script"] = os.path.join(script_dir, "install-jupyter-tmsn.sh")
        args["output"] = True
        is_worked = run_cluster(args, first_node_only=False)
        if not is_worked:
            return False
    elif total > 0:
        print("Cluster is not ready. Please check again later.")
        return False
    return True


def main_check_cluster():
    parser = argparse.ArgumentParser(
        description="Check the status of a cluster",
        usage="aws-jupyter check <args>",
    )
    parser.add_argument("--name",
                        required=False,
                        help="cluster name")
    parser.add_argument("--region",
                        help="Region name")
    parser.add_argument("--credential",
                        help="path to the credential file")
    config = vars(parser.parse_args(sys.argv[2:]))
    check_status_and_init(config)


if __name__ == '__main__':
    main_check_cluster()
