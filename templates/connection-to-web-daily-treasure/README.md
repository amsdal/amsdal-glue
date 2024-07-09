# Daily Treasure Web Connection

This example shows how to build a connection to the Daily Treasure web service using AMSDAL Glue.

This example demonstrates how to:

1. Initialize AMSDAL Glue
2. Define and register a connection to the Daily Treasure web service
3. Fetch all schemas/tables from connection
4. Fetch all data from the "daily_treasury_real_long_term_rate" table
5. Fetch data by date from the "daily_treasury_yield_curve" table

## Databases and data overview

The data source for this example is the Daily Treasury Yield Curve Rates and Daily Treasury Real Long-Term Rate from the
U.S. Department of the Treasury:
https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202407

Where each type of Interest Rate Data represent a separate table in the database dou to the different structure of the
data.

This example is not optimized for performance, but rather to demonstrate the capabilities of AMSDAL Glue.
This example uses the `httpx` library to fetch data from the web service.

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
