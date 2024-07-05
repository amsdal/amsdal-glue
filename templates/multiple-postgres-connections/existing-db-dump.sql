CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    age INT,
    country VARCHAR(50)
);

CREATE INDEX idx_full_name ON customers (first_name, last_name);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    item VARCHAR(100) NOT NULL,
    amount FLOAT NOT NULL,
    customer_id INT REFERENCES customers(customer_id)
);

ALTER TABLE orders
ADD CONSTRAINT check_amount_minimum
CHECK (amount >= 10);

INSERT INTO customers (customer_id, first_name, last_name, age, country) VALUES
(1, 'John', 'Doe', 31, 'USA'),
(2, 'Robert', 'Luna', 22, 'USA'),
(3, 'David', 'Robinson', 22, 'UK'),
(4, 'John', 'Reinhardt', 25, 'UK'),
(5, 'Betty', 'Doe', 28, 'UAE');

INSERT INTO orders (order_id, item, amount, customer_id) VALUES
(1, 'Keyboard', 400, 4),
(2, 'Mouse', 300, 4),
(3, 'Monitor', 12000, 3),
(4, 'Keyboard', 400, 1),
(5, 'Mousepad', 250, 2);
