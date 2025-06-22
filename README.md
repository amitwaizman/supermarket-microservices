# Supermarket Microservices System

### Overview  
An interactive microservices system simulating a supermarket network with 3 branches and 10 products for sale.  
The system consists of two services (applications):

- **App A (app_a)**: Simulates a cash register activity — each purchase is recorded in the `purchases` database table.  
- **App B (app_b)**: Provides real-time reports to the supermarket owner about customers and sales.


### Key Requirements  
- A network of 3 branches only.  
- Only 10 products available for sale.  
- Each customer can buy one unit of each product per purchase.  
- The system collects information on:  
  - Number of unique buyers in the network.  
  - List of loyal customers (those with at least 3 past purchases).  
  - Top 3 best-selling products (including ties).


### System Components  
- **db**: PostgreSQL database with `products` and `purchases` tables.  
- **app_a**: Microservice simulating cash register and inserting purchase data.  
- **app_b**: Microservice providing the supermarket owner dashboard reports.  
- **data_loader**: Utility for loading historic data from CSV files into the database.


### How to Run

1. Make sure Docker and Docker Compose are installed.  
2. Run the following command: 

   docker-compose up --build

3. The services will start automatically:

   * `app_a` simulates new purchases every 5 seconds.
   * `app_b` displays updated reports every 45 seconds.


### System Architecture Diagram

![aric1](https://github.com/user-attachments/assets/ce493533-48a8-4d69-a550-801ee951fd55)




