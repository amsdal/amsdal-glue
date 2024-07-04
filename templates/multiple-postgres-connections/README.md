# Multiple postgres connections

This example shows how to use AMSDAL Glue to connect to two postgres databases, one with existing tables and records, 
and another one with no tables.

This example demonstrates how to:

1. Initialize AMSDAL Glue
2. Register connections
3. Register a new schema/table in PostgreSQL database
4. Fetch all schemas/tables from both connections
5. Insert multiple records into `shipping` table
6. Fetch data by single command using joins for tables from different databases


## Databases and data overview

The existing database will contain the following tables and data:


### Table `customers`

| customer_id | first_name | last_name | age | country |
|-------------|------------|-----------|-----|---------|
| 1           | John       | Doe       | 31  | USA     |
| 2           | Robert     | Luna      | 22  | USA     |
| 3           | David      | Robinson  | 22  | UK      |
| 4           | John       | Reinhardt | 25  | UK      |
| 5           | Betty      | Doe       | 28  | UAE     |

### Table `orders`

| order_id | item      | amount | customer_id |
|----------|-----------|--------|-------------|
| 1        | Keyboard  | 400    | 4           |
| 2        | Mouse     | 300    | 4           |
| 3        | Monitor   | 12000  | 3           |
| 4        | Keyboard  | 400    | 1           |
| 5        | Mousepad  | 250    | 2           |

In this example we will also create a new `shipping` table with the following data in a second database:

### Table `shipping`

| shipping_id | status    | customer_id |
|-------------|-----------|-------------|
| 1           | Pending   | 2           |
| 2           | Pending   | 4           |
| 3           | Delivered | 3           |
| 4           | Pending   | 5           |
| 5           | Delivered | 1           |

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
