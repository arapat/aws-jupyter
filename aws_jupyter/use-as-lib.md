# Use aws-jupyter as a python module

This document describe how to integrate `aws-jupyter` into your Python program as a module.

## Basic usage

There is a method that corresponds to each `aws-jupyter` command. All commands receive one
dictionary-type parameter `args`, which contains the parameters required for the corresponding
command.

## Check if AWS access credentials work `$ aws-jupyter access`

```python
from aws_jupyter.credentials import check_access
check_access({})
```

## Create a cluster using EC2 instances `$ aws-jupyter create`

```python
from aws_jupyter.create_cluster import main_create_cluster
```

## Check cluster status `$ aws-jupyter check`

```python
from aws_jupyter.check_cluster import check_status_and_init

check_status_and_init({
    "name": "cluster-name",
})
```

## Terminate a cluster `$ aws-jupyter terminate`

```python
from aws_jupyter.credentials import main_check_access
```

## Run a script `$ aws-jupyter run`

```python
from aws_jupyter.run_cluster import main_run_cluster
```

## Retrieve files `$ aws-jupyter retrieve`

```python
from aws_jupyter.retrieve_files import main_retrieve_files
```

##  Send a local directory to the instances `$ aws-jupyter send-dir`

```python
from aws_jupyter.send_files import main_send_files
```