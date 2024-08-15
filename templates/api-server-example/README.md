# API Server example

This example show how to easily create a REST API server using AMSDAL Glue on top of existing data sources.

## Databases and data overview

### Database `customers_and_products.sqlite3`

#### Table `customers`

This is a simple table with customer information.

| Field name  | Field type   |
|-------------|--------------|
| customer_id | INTEGER (FK) |
| name        | TEXT         |
| email       | TEXT         |

| customer_id | name | email             |
|-------------|------|-------------------|
| 1           | John | test1@example.com |
| 2           | Jane | test2@example.com |
| 3           | Jack | test3@example.com |

#### Table `products`

This is another simple table with product information.

| Field name | Field type   |
|------------|--------------|
| product_id | INTEGER (PK) |
| name       | TEXT         |
| price      | REAL         |

| product_id | name     | price |
|------------|----------|-------|
| 1          | Keyboard | 150   |
| 2          | Mouse    | 100   |
| 3          | Monitor  | 700   |


#### Table `profiles`

This table contains customer profiles. This table has a foreign key to the `customers`
table, and also do not have a primary key.

| Field name  | Field type |
|-------------|------------|
| profile_id  | INTEGER    |
| customer_id | INTEGER    |
| address     | TEXT       |
| phone       | TEXT       |

| profile_id | customer_id | address | phone |
|------------|-------------|---------|-------|
| 1          | 1           | USA     | 123   |
| 2          | 2           | UK      | 456   |
| 3          | 3           | USA     | 789   |


### Database `orders.sqlite3`

#### Table `orders`

Table with order information. It has contraint for quantity field to be greater than 0.

| Field name  | Field type   |
|-------------|--------------|
| order_id    | INTEGER (PK) |
| product_id  | INTEGER      |
| customer_id | INTEGER      |
| quantity    | INTEGER      |

| order_id | product_id | customer_id | quantity |
|----------|------------|-------------|----------|
| 1        | 1          | 1           | 2        |
| 2        | 2          | 2           | 3        |
| 3        | 3          | 3           | 1        |
| 4        | 1          | 2           | 1        |
| 5        | 2          | 1           | 1        |
| 6        | 3          | 2           | 2        |


#### Table `cart`

This table is similar to the `orders` table, but it has a composite primary key.

| Field name  | Field type   |
|-------------|--------------|
| cart_id     | INTEGER (PK) |
| product_id  | INTEGER (PK) |
| customer_id | INTEGER      |

| product_id | customer_id | quantity |
|------------|-------------|----------|
| 1          | 1           | 1        |
| 2          | 2           | 2        |
| 3          | 3           | 3        |


### Database `logs.sqlite3`

#### Table `logs`

Table with log messages.

| Field name | Field type |
|------------|------------|
| message    | TEXT       |
| created_at | TIMESTAMP  |

| message | created_at          |
|---------|---------------------|
| Info    | 2022-01-01 10:00:00 |
| Error   | 2022-01-01 11:00:00 |
| Warning | 2022-01-01 12:00:00 |


## Quick start

### Step 1 [Optional]: Create a virtual environment

Open a terminal and run the following command:

```bash
python3 -m venv .venv-example 
```

It will create the `.venv-example` folder in the current directory.
Now, let's activate the virtual environment:

```bash
source .venv-example/bin/activate
```

### Step 2: Install the required packages

Now, let's install `amsdal-glue-api-server` package and its dependencies. 
In terminal, make sure you are in the current directory and you have activated the virtual environment, run the 
following command:

```bash
pip install -r requirements.txt
```

### Step 3: Run example

Now we are ready to run the server:

```bash
python3 main.py
```

After this you should be able to access the Swagger at [http://localhost:8000/docs](http://localhost:8000/docs).

There you will find the following sections:

 - REST - REST API endpoints for each of the tables. All of the schemas will have create (POST) and read (GET) operations. Tables with primary keys will also have update (PUT) and delete (DELETE) operations.
 - Operations - List of endpoints that accept amsdal-glue like data structures as input and output. Please check the [amsdal-glue documentation](https://amsdal.com/docs/amsdal-glue/) and [Swagger](http://localhost:8000/docs) for more information.
 - SQL - There is only one endpoint that accepts SQL query as input and uses amsdal-glue-sql-parser to parse the query and execute it on the database.