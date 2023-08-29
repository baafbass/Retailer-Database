#                         Setting up the SQLİTE database 
import sqlite3

# Connect to SQlite database
conn = sqlite3.connect('retailer.db')

# Creating a cursor object allows us to execute SQL command
c = conn.cursor()

# Enabling foreign key support in SQlite
c.execute("PRAGMA foreign_keys = ON")

# Create the 'Customers' table
c.execute('''
CREATE TABLE IF NOT EXISTS Customers(
customerID INTEGER PRIMARY KEY,
firstName TEXT NOT NULL,
lastName TEXT NOT NULL,
birthDate DATE,
moneySpent REAL,
anniversary DATE
)
''')

conn.commit()

# Create the 'Employees' table
c.execute('''
CREATE TABLE IF NOT EXISTS Employees(
employeeID INTEGER PRIMARY KEY,
firstName TEXT NOT NULL,
lastName TEXT NOT NULL,
birthDate DATE
)
''')

conn.commit()

# Create the 'Products' table
c.execute('''
CREATE TABLE IF NOT EXISTS Products(
productID INTEGER PRIMARY KEY,
category TEXT,
price REAL
)
''')

conn.commit()

# Create the 'Orders' table
c.execute('''
CREATE TABLE IF NOT EXISTS Orders(
orderID INTEGER PRIMARY KEY,
customerID INTEGER,
employeeID INTEGER,
productID INTEGER,
orderTotal REAL,
orderDate Date,

FOREIGN KEY(customerID) REFERENCES Customers(customerID),
FOREIGN KEY(employeeID) REFERENCES Employees(employeeID),
FOREIGN KEY(productID) REFERENCES Products(productID)
)
''')

# Commit the changes made to the Database
conn.commit()
# Close the connection to the database
conn.close()

#                       Inserting Sample Data

# sample data for customers (without the anniversary field)
customers_data = [(1, 'John', 'Doe', '1990-05-15', 1200, None),
                  (2, 'Jane', 'Smith', '1985-08-20', 900, None),
                  (3, 'Alice', 'Johnson', '2000-03-10', 1050, None),
                  (4, 'Bob', 'Miller', '1995-10-25', 750, None),
                  (5, 'Charlie', 'Brown', '1980-01-28', 1300, None),
                  (6, 'David', 'Clark', '1975-02-17', 500, None),
                  (7, 'Eva', 'Martin', '1998-12-12', 1100, None),
                  (8, 'Frank', 'White', '1982-06-30', 850, None),
                  (9, 'Grace', 'Lee', '1999-04-17', 950, None),
                  (10, 'Henry', 'Garcia', '1992-07-23', 700, None)]

#Anniversary column will be added to the anniversary data will be computed later based on the order data

# Sample data for Employees
employees_data = [(1, 'Ella', 'Wright', '1990-04-14'),
                  (2, 'Oliver', 'Harris', '1982-09-19'),
                  (3, 'Lucas', 'Robinson', '1978-02-02'),
                  (4, 'Mia', 'Hall', '1988-11-11'),
                  (5, 'Ava', 'Wood', '1995-06-06'),
                  (6, 'Sophia', 'Turner', '1985-12-15'),
                  (7, 'Liam', 'Anderson', '1992-03-03'),
                  (8, 'Noah', 'Allen', '1987-08-08'),
                  (9, 'Emma', 'Young', '1993-07-07'),
                  (10, 'Benjamin', 'Hernandez', '1979-05-05')]

# Sample data for Products
products_data = [(1, 'Electronics', 200), (2, 'Clothing', 50),
                 (3, 'Groceries', 30), (4, 'Electronics', 150),
                 (5, 'Books', 20), (6, 'Clothing', 100), (7, 'Books', 15),
                 (8, 'Electronics', 250), (9, 'Groceries', 40),
                 (10, 'Books', 25)]

# Sample data for orders
# Import required libraries :
# -randint and choice are used to generate random numbers and select random items form a list respectively
# datetime and timedelta are used to work with date and time

from random import randint, choice
from datetime import datetime, timedelta

# Initialzing an empty list to store the generated order data
orders_data = []

# Loop to generate data for 10 orders

for i in range(1, 11):

  # Select a random customer ID from the customers_data list.
  customer = choice(customers_data)[0]
  # Select a random employee ID from the employee_data list.
  employee = choice(employees_data)[0]
  # Select a random product ID from the product_data list.
  product = choice(products_data)[0]

  # Generate a random order total value from 20 to 250.
  order_total = randint(20,250)

  # Generate a random date within the past year for the order data.
  # The timedelta with randint(0,365) provides a random number of days within a year.
  # The resulting day is then formatted to 'YYYY-MM-DD'.
  order_date = (datetime.now() - timedelta(days = randint(0,365))).strftime('%Y-%m-%d')

  # Append the generated order details to the orders_data list.
  orders_data.append((i,customer,employee,product,order_total,order_date))

# Inserting the data into tables
conn = sqlite3.connect('retailer.db')
c = conn.cursor()

c.executemany(
  "INSERT INTO Customers VALUES(?,?,?,?,?,?)",customers_data
)

c.executemany(
  "INSERT INTO Employees VALUES(?,?,?,?)", employees_data
)

c.executemany(
  "INSERT INTO Products VALUES(?,?,?)", products_data
)
c.executemany(
  "INSERT INTO Orders VALUES(?,?,?,?,?,?)", orders_data
)

# Commit the changes
conn.commit()

#                      Updating The anniversary field

# Define a SQL Query to update the 'anniversary' field for each customer.

update_anniversary_query = """
UPDATE Customers
SET anniversary = (
   SELECT strftime('%Y-%m-%d',
          strftime('%Y',DATE(MIN(orderDate), '+1 year')) || '-' ||
          strftime('%m',MIN(orderDate)) || '-' ||
          strftime('%d',MIN(orderDate)))
    FROM Orders
    WHERE Orders.customerID = Customers.customerID
)
"""

# Execute the SQL query using the cursor to update the 'anniversary' field in the Customers table
c.execute(update_anniversary_query)


                          #Identify and Reward Top Customers

spending_goal = 1000 # for example

top_customers_query = f"""
SELECT customerID,firstName,lastName,moneySpent FROM Customers 
WHERE moneySpent >= {spending_goal} ORDER BY moneySpent DESC
"""

top_customers = c.execute(top_customers_query)
data = top_customers.fetchall()
print(data)
print("\n")
#                        Gift Customers on their 1-year Purchase Anniversary

from datetime import datetime,timedelta

# Get the current date
current_date = datetime.now().date()

# Calculate the start and end dates for the upcoming anniversary window
start_date = current_date
end_date = current_date + timedelta(days = 7)  # Assuming a 7 day window to identify upcoming anniversaries

# SQL query to identify customers with an upcoming 1-year purchase anniversary within the window

upcoming_anniversary_query = f"""
SELECT customerID,firstName,lastName, anniversary FROM Customers WHERE anniversary BETWEEN '{start_date}' and '{end_date}'
"""

# Execute the query and fetch the results
upcoming_anniversaries = c.execute(upcoming_anniversary_query).fetchall()
print(upcoming_anniversaries)
print("\n")
conn.commit()

# Fetch and Display the table content using pandas
import pandas as pd
conn = sqlite3.connect('retailer.db')

query = "SELECT * FROM Customers"
df = pd.read_sql(query,conn)
print(df)
print("\n")

#                       Organize products by price and Category

product_query = "SELECT category,productID,price FROM Products ORDER BY category,price DESC"
organized_product = c.execute(product_query).fetchall()
print(organized_product)
print("\n")
#                        Track Best Performing Employees

# Define a SQL query to identify the top-performing employees
# The goal is to :
# - Join Employees and Orders tables using employeeID
# - Sum the total sales for each employee.
# - Rank the employees based on their total sales in descending order.
# - Retrieve only the top 5 employees with the highest sales.

top_employee_query = """
SELECT e.employeeID,e.firstName,e.lastName, SUM(o.orderTotal) as TotalSales FROM Employees e JOIN Orders o ON e.employeeID = o.employeeID GROUP BY e.employeeID ORDER BY TotalSales DESC LIMIT 5
"""

# Execute the SQL query using the cursor to retrieve the top 5 employees based on sales
top_employees = c.execute(top_employee_query).fetchall()
print(top_employees)