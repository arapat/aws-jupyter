This is a quick-start guide for running Jupyter on AWS.
It is an example to show what you can do with `aws-jupyter`.
You can also try this example by running `launch-aws-jupyter` in the command line,
which will prompt a step-by-step guide to walk you through this example.

Please read [README](README.md) for more information.


## Run Jupyter on AWS

0. Check configuration

```bash
aws-jupyter config
```

1. Start the cluster

```bash
aws-jupyter create -c 1 --name jupyter
```

To speicify a custom AMI image, append "--ami <ami_id>" to the cluster creation command above.

2. Check the cluster is up

```bash
aws-jupyter check --name jupyter
```

3. Open the URL printed out in the Step 3.

4. Shut down the instance

```bash
aws-jupyter terminate --name jupyter
```

6. To SSH into the first node, run

```bash
aws-jupyter ssh --name jupyter
```

## Run tmsn

1. First run the tmsn example

```bash
aws-jupyter run -s examples/tmsn-example.py
```

2. Retrieve outputs from the nodes in the cluster

```bash
mkdir _files
aws-jupyter retrieve --remote /tmp/std* --local _files
```

3. Check the outputs

```bash
cat _files/worker-0/stdout.log
cat _files/worker-1/stdout.log
```

## Setup and Diagnose

1. Print diagnose information to debugging

```bash
aws-jupyter diagnose
```

