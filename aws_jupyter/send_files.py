#!/usr/bin/env python
import argparse
import os
import subprocess
import sys

from .common import load_config
from .common import check_connections


def check_exists(path):
    return os.path.isfile(path) 


def parse_file_path(path):
    return (path, path.rsplit('/', 1)[1])


def send_files(args):
    if not check_exists(args["key_path"]):
        print("Error: File '{}' does not exist.".format(args["key_path"]))
        return
    if not check_exists(args["neighbors"]):
        print("Error: File '{}' does not exist.".format(args["neighbors"]))
        return
    if not os.path.isdir(args["local"]):
        print("Error: Local directory '{}' does not exist.".format(args["local"]))
        return

    with open(args["neighbors"]) as f:
        status = f.readline()
        if status[0] != 'R':  # Not "Ready."
            print("Please run `check-cluster.py` first and "
                  "make sure all instances in the cluster is up and running.")
            return
        instances = [t.strip() for t in f if t.strip()]

    # Send the files
    key = args["key_path"]
    local_path = args["local"]
    remote_path = args["remote"]
    if os.path.expanduser("~") in remote_path:
        remote_path = remote_path.replace(os.path.expanduser("~"), ".")
    if not check_connections(instances, args):
        return
    for url in instances:
        print("Sending the config file to '{}'".format(url))
        command = ("ssh -o StrictHostKeyChecking=no -i {} ubuntu@{} \"mkdir -p {}\"; "
                   "").format(key, url, remote_path)
        command += ("scp -o StrictHostKeyChecking=no -i {} -r {} ubuntu@{}:{}"
                    "").format(key, local_path, url, remote_path)
        subprocess.run(command, shell=True, check=True)
    print("Done.")


def main_send_files():
    parser = argparse.ArgumentParser(
        description="Send a local directory to the cluster")
    parser.add_argument("--local",
                        required=True,
                        help="Path of the local directory that contains "
                             "all the files to be uploaded")
    parser.add_argument("--remote",
                        required=True,
                        help="Path of the remote directory to which the files will be uploaded")
    parser.add_argument("--credential",
                        help="path to the credential file")
    args = vars(parser.parse_args(sys.argv[2:]))
    args["neighbors"] = os.path.abspath("./neighbors.txt")
    config = load_config(args)
    send_files(config)


if __name__ == '__main__':
    main_send_files()
