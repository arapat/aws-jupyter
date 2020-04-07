# aws-jupyter manual

`aws-jupyter` is a command-line tool to run Jupyter on AWS. It can be used to create EC2 instances,
install Jupyter and [tmsn](https://github.com/arapat/tmsn) on the instances, and terminate the
instances.

## Credential files

First of all, create a credential file in the YAML format:

```
any_name_you_like:
    key_name: your_aws_key_pair_name
    ssh_key: /path/to/the/aws/key/file
    access_key_id: your_aws_key_id
    secret_access_key: your_aws_secret_access_key
```

Save this file to a secure location, and set the location of this file as the value of the
`--credential` argument (read below).

For example, your credential file might look like this:

```
> cat ./aws-jupyter-credential.yml
my_main_project:
    key_name: my-aws-key
    ssh_key: /home/casey/vault/my-aws-key.pem
    access_key_id: WOIPODOJOJDAAXXIOJQWE
    secret_access_key: sDurjb4402948-e859+9289rEzzeoi778z98fe1q
```

The file provides two types of access tokens to your AWS account,

* your security credentials; learn how to create one at
[Managing Access Keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)
* your EC2 key pair; learn how to create one at
[Creating a Key Pair Using Amazon EC2](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/ec2-key-pairs.html#having-ec2-create-your-key-pair)

The EC2 key pairs are region-specific: you cannot create EC2 instances in `us-east-1`
using a key pair created in `us-west-1`.
At this moment, `aws-jupyter` only supports the `us-west-2` region.


## Supported commands

`aws-jupyter` supports following commands:
"config", "access", "create", "check", "terminate", "run", "ssh", "retrieve", "send-dir", "diagnose".

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

## Check if AWS access credentials work

`> aws-jupyter access`

Check if the AWS credentials work. If not, we will print an error message.


## Create a cluster using EC2 instances

`> aws-jupyter create`

Crate a cluster using AWS spot instances

If the instance comes with attached SSD, it will be mounted to `/mnt`.

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
and starts it on all the EC2 instances.

By default, it doesn't check if the script started successfully,
neither does it wait till the scripts to finish. It will, however, redirect the stderr and stdout
of the scripts to `/tmp/stdout` and `/tmp/stderr`. Later, you can retrieve these two files
using the `aws-jupyter retrieve` command (see below) and check the script output.

If the `--output` argument is set, the scripts will run on the EC2 instances sequentially (i.e. the
script does not launch on the next instance until the current one finished executing). Furthermore,
it will print the script output to the commandline directly.

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

`> aws-jupyter send-dir`

Send a local directory to the cluster

```
usage: aws-jupyter [-h] --local LOCAL --remote REMOTE
                   [--credential CREDENTIAL]

optional arguments:
  -h, --help            show this help message and exit
  --local LOCAL         Path of the local directory that contains all the
                        files to be uploaded
  --remote REMOTE       Path of the remote directory to which the files will
                        be uploaded
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


## Print help message

`aws-jupyter --help`
