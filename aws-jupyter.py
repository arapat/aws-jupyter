#!/usr/bin/env python3

from lib.create_cluster import main_create_cluster
from lib.check_cluster import main_check_cluster
from lib.run_cluster import main_run_cluster, run_cluster
from lib.terminate_cluster import main_terminate_cluster
from lib.set_config import main_set_config
from lib.ssh_headnode import main_ssh_headnode
import argparse
import sys


class AwsJupyter:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Launch Jupyter on AWS",
            usage="aws-jupyter.py <task> [<args>]\nRun with -h to see supported tasks",
        )
        parser.add_argument(
            "task",
            help="Task to perform, should be one of 'config', 'create', 'check', 'terminate'")
        config = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, config.task):
            print("Error: Cannot reconize the task type '{}'.".format(config["task"]))
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, config.task)()

    def config(self):
        main_set_config()

    def create(self):
        main_create_cluster()

    def check(self):
        (config, status) = main_check_cluster()
        if status is None:
            ready, total = 0, 0
        else:
            ready, total = status
        if ready > 0 and ready == total:
            print("Cluster is running (yet might still being initialized). \
                   I will try to start Jupyter notebook now.")
            config["files"] = ["./neighbors.txt"]
            config["script"] = "./script-examples/install-jupyter-tmsn.sh"
            config["output"] = True
            run_cluster(config)
        elif total > 0:
            print("Cluster is not ready. Please check again later.")

    def terminate(self):
        main_terminate_cluster()

    def run(self):
        main_run_cluster()

    def ssh(self):
        main_ssh_headnode()

if __name__ == '__main__':
    AwsJupyter()
