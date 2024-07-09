# AMSDAL Glue SQL Parser Usage

This example shows how to use AMSDAL Glue to use SQL Parser with multiple postgres connections, one with existing tables and records,

This example demonstrates how to:

1. Initialize AMSDAL Glue
2. Register connections
3. Register a new schemas/tables in PostgreSQL database
4. Add data to the tables
5. Fetch data by single command using joins for tables from different databases
6. Fetch data with aggregations and filters


## Databases and data overview

In this example we will create a new `customers` and `orders` tables in different databases:


### Table `customers`

| id | first_name | last_name |
|----|------------|-----------|
| 1  | John       | Doe       |
| 2  | Jane       | Smith     |
| 3  | Alice      | Johnson   |
| 4  | Bob        | Brown     |

### Table `orders`

| id | product    | price  | customer_id |
|----|------------|--------|-------------|
| 1  | Laptop     | 1000   | 1           |
| 2  | Phone      | 500    | 2           |
| 3  | Tablet     | 800    | 3           |
| 4  | Headphones | 200    | 3           |



## Quick start

We will run two postgres databases in docker containers, so make sure you have installed Docker locally.


### Step 1: Run the databases

Let's run the two postgres databases in docker containers. 
Open a separate terminal, go to current directory and run the following command:

```bash
docker compose up
```

It will start both postgres databases, one with existing tables and data and empty one.

### Step 2 [Optional]: Create a virtual environment

Open a terminal and run the following command:

```bash
python3 -m venv .venv-example 
```

It will create the `.venv-example` folder in the current directory.
Now, let's activate the virtual environment:

```bash
source .venv-example/bin/activate
```

### Step 3: Install the required packages

Now, let's install `amsdal-glue` package and its dependencies. 
In terminal, make sure you are in the current directory and you have activated the virtual environment, run the 
following command:

```bash
pip install -r requirements.txt
```

### Step 4: Run example

Now we are ready to run our examples:

```bash
python3 main.py
```
