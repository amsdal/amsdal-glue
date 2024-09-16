# CQRS Example

This example demonstrates how to use AMSDAL Glue to work with multiple databases and perform CQRS operations.

## Quick start

We will run two postgres databases in docker containers, so make sure you have installed Docker locally.


### Step 1: Run the databases

Let's run the two postgres databases in docker containers. 
Open a separate terminal, go to current directory and run the following command:

```bash
docker compose up
```

It will start both postgres databases, one with existing tables and data and empty one.

Now, you can run jupyter notebook and execute the example notebook.
