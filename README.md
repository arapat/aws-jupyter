This script launches a cluster on AWS EC2 instances and starts a Jupyter notebook on them.

Please read the [manual](manual.md) for the details of all supported commands.
[QuickStartGuide.md](QuickStartGuide.md) offers a guided example to show what `aws-jupyter` can do.

## Install

Pleasure ensure you have Python 3. `aws-jupyter` can be install using `pip`:

```
pip install aws-jupyter
```

After the installation, you can try it out using the example launch script:

```
launch-aws-jupyter
```

It will create a cluster with 2 spot instances.

In addition,
we create the EC2 instances using an AMI image that located in the region `us-west-2`.
So please make sure that your local environment is set up to use that region
(you can run `aws-jupyter config` to verify the setting).

After installation, please run `aws-jupyter config` to make sure the configuration is properly set.


## Upgrade

In case we change the default AWS region, please upgrade `aws-jupyter` in 3 steps:

1. Upgrade the package: `pip install --upgrade aws-jupyter`.
2. Create the new key pair in the new AWS region, and modify the "key_name" and "ssh_key" fields of
the credential file accordingly (read below).
3. Switch to default AMI and region: `aws-jupyter config --default-ami --default-region`, and set the credential file
to the location of the new one when prompted.


### AWS Credential

The scripts in this repository requires a `credentials.yml` file in following format:

```yaml
Arbitrary Name:
  access_key_id: your_aws_access_key_id
  secret_access_key: your_aws_secret_access_key
  key_name: your_ec2_key_pair_name
  ssh_key: /path/to/the/ec2/key/pair/file
```

The credential file in the Spark Notebook project can be directly used here.

The credential file (or a soft link to it) should be located in the same folder where
you invoke these scripts (i.e. you should be able to see it using `ls .` command).
The credential file must always **stay private** and not be shared. Remember to add
`credential.yml` to the `.gitignore` file of your project so that this
file would not be pushed to GitHub.


## Usage

Run any script in this directory with `-h` argument will print the help message of the script.


### Create a new cluster

`aws-jupyter create` creates a cluster on the `m3.xlarge` instance using an AMI based on Ubuntu.

#### Example:

```bash
aws-jupyter create -c 2 --name testing
```


### Check if a cluster is ready

`aws-jupyter check` checks if a cluster is up and running. In addition, it also creates a
`neighbors.txt` file which contains the IP addresses of all the instances in the cluster.

#### Example

```bash
aws-jupyter check --name testing
```


### Terminate a cluster

`aws-jupyter terminate` terminates a cluster by stopping and terminating all instances
in this cluster.

#### Example
```bash
aws-jupyter terminate --name testing
```


### Run a script on a cluster

`aws-jupyter run` runs a given script on all instances in the cluster.
It starts the script in the background, and redirect the stdout/stderr
into a file on the instances which can be checked later.
Thus it terminates does not necessarily mean the script has finshed executing on the cluster.
In addition, it only launches the script on all instances, but does _not_ check if the script
executes without error.

#### Example
```bash
aws-jupyter run --script ./script-examples/hello-world.sh
```


### Send configuration files to all instances in a cluster

In most cases, we would like the different workers/instances in a cluster run with
different parameters. We can achieve that by generating a different configuration file
for each worker, and letting the program read its parameter from this file.
The script `send-configs.py` is used for sending the configuration files to the workers.
Please refer to the Find Prime Number examples in `/example` for the demonstration of using
this script.

#### Example
After generating a cluster with `N` workers, one can write a custom script to generate `N`
configuration files, one for each worker, and save all configuration files in the some directory
(e.g. `./example-configs/`). After that, run following command

```bash
aws-jupyter send-configs --config ./example-configs/
```


## Retrieve files from all instances in a cluster

`retrieve-files.py` retrieve files from the same location on all instances of a cluster.
It can be used to collect the output of the program from the workers.
A local directory for saving the downloaded files should be provided to this script.
This script will create a separate sub-directory for each worker and download its files
to this sub-directory.

### Example
```bash
mkdir _result
aws-jupyter retrieve --remote /tmp/std* --local ./_result/
```

## Install a package on all instances

You can install any missing packages *after the instances are ready* (i.e. `aws-jupyter check` shows Jupyter notebook URL) by following these step:

1. create a script on your local computer, which install the required package. For example, assume we want to install `pandas`,

```bash
$ echo "pip install pandas" > install-pandas.sh
````

2. run the script on all instances

```bash
aws-jupyter run -s install-pandas.sh --output
```

The `--output` argument ensures that the script will run in foreground, so that you can check if the installation succeed.
