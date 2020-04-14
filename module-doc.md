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
from aws_jupyter.create_cluster import create_cluster

create_cluster({
    "count": 2,
    "name": "cluster-name",
    "type": "r3.large",
})
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
from aws_jupyter.credentials import terminate_cluster
terminate_cluster({
    "name": "cluster-name",
})
```

## Run a script `$ aws-jupyter run`

```python
from aws_jupyter.run_cluster import run_cluster
run_cluster({
    "script": "/path/to/the/script",
})
```

## Retrieve files `$ aws-jupyter retrieve`

```python
from aws_jupyter.retrieve_files import retrieve_file
retrieve_file({
    "remote": "/a/list/of/the/filepaths/to/the/file/on/the/cluster",
    "local": "/local/directory/to/save/the/files",
})
```

##  Send a local directory to the instances `$ aws-jupyter send-dir`

```python
from aws_jupyter.send_files import send_files
send_files({
    "local": "/local/directory/path/to/send/to/the/cluster",
    "remote": "/localtion/of/the/directory/on/the/cluster/to/save/the/files",
})
```
