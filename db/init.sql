-- Delete existing tables 
DROP TABLE IF EXISTS purchases;
DROP TABLE IF EXISTS products;

-- Create a product table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL
);

-- Create a purchase table
CREATE TABLE purchases (
    id SERIAL PRIMARY KEY,
    supermarket_id VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    user_id UUID NOT NULL,
    items TEXT[] NOT NULL,
    total_amount REAL NOT NULL
);
