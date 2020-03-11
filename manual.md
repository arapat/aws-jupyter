# aws-jupyter manual

`aws-jupyter` is a command-line tool to run Jupyter on AWS. It can be used to create EC2 instances,
install Jupyter and [tmsn](https://github.com/arapat/tmsn) on the instances, and terminate the
instances.

## Supported commands

`aws-jupyter` supports following commands:
"config", "create", "check", "terminate", "run", "ssh", "retrieve", "send-configs", "diagnose".

## Set basic configurations

`> aws-jupyter config`

Set basic configuration, such as the AWS region, and the location of the credential file.

```
usage: aws-jupyter config <args>

optional arguments:
  -h, --help            show this help message and exit
  --region REGION       region name
  -t TYPE, --type TYPE  the type of the instances
  --ami AMI             AMI type
  --credential CREDENTIAL
                        path to the credential file
```

`aws-jupyter` creates a configuration file at `~/.tmsn_config`. You don't need to edit this file.
It stores the last configuration parameters and reuse them for next time, for example,
you can create a cluster with `aws-jupyter create --name test-cluster`, and check it
status by running `aws-jupyter check` instead of `aws-jupyter check --name test-cluster`.


## Create a cluster using EC2 instances

`> aws-jupyter create`

Crate a cluster using AWS spot instances

```
usage: aws-jupyter create [<args>]

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        the number of instances in the cluster
  --name NAME           cluster name
  -t TYPE, --type TYPE  the type of the instances
  --region REGION       Region name
  --ami AMI             AMI type
  --credential CREDENTIAL
                        path to the credential file
  --spot SPOT           the max price for spot instances, if not set, will use
                        on-demand instances
```

## Check cluster status

`> aws-jupyter check`

Check the status of a cluster.
Use this command after running `aws-jupyter check` to see if the cluster is up and running.

```
usage: aws-jupyter check <args>

optional arguments:
  -h, --help            show this help message and exit
  --name NAME           cluster name
  --region REGION       Region name
  --credential CREDENTIAL
                        path to the credential file
```

## Terminate a cluster

`> aws-jupyter terminate`

Terminate a cluster, i.e. shutting down all its instances.

```
usage: aws-jupyter config <args>

optional arguments:
  -h, --help            show this help message and exit
  --name NAME           cluster name
  --region REGION       Region name
  --credential CREDENTIAL
                        path to the credential file
```


## Run a script

`> aws-jupyter run`

Run a script on all instances of a cluster. It uploads your script (as specified by the `-s` parameter)
and starts it on all the EC2 instances. Note that it doesn't check if the script started successfully,
neither does it wait till the scripts to finish. It will, however, redirect the stderr and stdout
of the scripts to `/tmp/stdout` and `/tmp/stderr`. Later, you can retrieve these two files
using the `aws-jupyter retrieve` command (see below) and check the script output.

```
usage: aws-jupyter run [<args>]

optional arguments:
  -h, --help            show this help message and exit
  -s SCRIPT, --script SCRIPT
                        File path of the script that needs to run on the
                        cluster
  --files FILES [FILES ...]
                        File path of the file that needs to be sent to the
                        instances. For multiple files, separate them using
                        spaces.
  --output              If set, wait till the script exits on the instances
                        and print its output to the commandline. Otherwise,
                        run the script in the background and redirect the
                        stdout/stderr of the script to a log file on the
                        instance.
  --credential CREDENTIAL
                        path to the credential file
```


## SSH into the head node of a cluster

`> aws-jupyter ssh`

SSH into the head node of a cluster. You might want to use this command to check if the script
uploaded using `aws-jupyter run` has finished execution.

```
usage: aws-jupyter config <args>

optional arguments:
  -h, --help            show this help message and exit
  --name NAME           cluster name
  --region REGION       Region name
  --credential CREDENTIAL
                        path to the credential file
```


## Retrieve files

`> aws-jupyter retrieve`

Retrieve the files from the instances of a cluster

```
usage: aws-jupyter [-h] --remote REMOTE [REMOTE ...] --local LOCAL


optional arguments:
  -h, --help            show this help message and exit
  --remote REMOTE [REMOTE ...]
                        Path of the remote files to be downloaded. For
                        multiple files, separate them using spaces
  --local LOCAL         Path of the local directory to download the remote
                        files
  --credential CREDENTIAL
                        path to the credential file
```


##  Send different configuration files to the instances

`> aws-jupyter send-configs`

Send a different configuration file to each instance of a cluster

```
usage: aws-jupyter [-h] --config CONFIG [--credential CREDENTIAL]

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Path of the directory that contains all configuration
                        files
  --credential CREDENTIAL
                        path to the credential file
```


## Print diagnose info on an exsting cluster

`> aws-jupyter diagnose`

This command is used for debugging purpose. You can send the output printed out by the command
to us for the debugging purpose.


```
usage: aws-jupyter [-h] [--name NAME] [--credential CREDENTIAL]


optional arguments:
  -h, --help            show this help message and exit
  --name NAME           cluster name
  --credential CREDENTIAL
                        path to the credential file
  --region REGION       Region name
```


## `aws-jupyter --help`

Print the help message
