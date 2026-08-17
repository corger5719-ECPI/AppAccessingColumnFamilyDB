# Amazon Cassandra CRUD Application

## Assignment

**Name:** Cora Germany  
**Date:** August 16, 2026  
**Assignment:** Cassandra CRUD Application  

## Purpose

This Python application demonstrates how to use CRUD operations with an Apache Cassandra database. The program uses the `cassandra-driver` Python library to connect to Cassandra and sends CQL commands to create and manage the required keyspace and tables.

The application creates an `Amazon` keyspace and works with two tables:

- `Reviews`
- `ProductCategories`

The program also reads review data from a JSON file and inserts the data into both Cassandra tables.

## Requirements

Before running the program, make sure the following are installed and running:

- Python 3
- Apache Cassandra
- `cqlsh`
- `cassandra-driver`
- A JSON review dataset

Install the Cassandra Python driver with:

```bash
python3 -m pip install cassandra-driver
```

## Cassandra Connection

The program connects to Cassandra on the local computer using:

```python
Cluster(["127.0.0.1"])
```

Cassandra must be running before starting the Python application.

You can test the Cassandra connection by entering:

```bash
cqlsh
```

At the `cqlsh>` prompt, view available keyspaces with:

```sql
DESCRIBE KEYSPACES;
```

Type the following to leave `cqlsh`:

```sql
exit;
```

## How to Run the Program

1. Save the Python file as `Amazon_Cassandra_CRUD.py`.
2. Place the Python file and JSON dataset in the same folder, if possible.
3. Open a Linux/Ubuntu terminal.
4. Change to the folder containing the Python file.
5. Run:

```bash
python3 Amazon_Cassandra_CRUD.py
```

Do not run the Python file from inside the `cqlsh>` prompt.

## Program Features

The application menu allows the user to:

1. Create the `Amazon` keyspace.
2. Create the `Reviews` table.
3. Create the `ProductCategories` table.
4. Insert JSON data into both tables.
5. Display all distinct product categories.
6. Display the count of reviews with 4 stars or higher for a user-entered product category.
7. Display the count of 1-star reviews for a user-entered product category.
8. Type and execute a CQL `SELECT` statement.
9. Add a column to the `Reviews` or `ProductCategories` table.
10. Remove a column from the `Reviews` or `ProductCategories` table.
11. Delete the `Reviews` or `ProductCategories` table.
12. Delete the `Amazon` keyspace.
13. Exit the program.

## Keyspace

The program creates the required Cassandra keyspace named:

```text
Amazon
```

Cassandra normally displays an unquoted keyspace name in lowercase, so it may appear in `cqlsh` as:

```text
amazon
```

The keyspace uses `SimpleStrategy` with a replication factor of `1` for the local classroom environment.

## Reviews Table

The `Reviews` table contains:

- `review_id`
- `product_id`
- `reviewer_id`
- `stars`
- `review_body`
- `review_title`
- `product_category`

The `review_id` field is used as the primary key.

## ProductCategories Table

The `ProductCategories` table contains:

- `product_id`
- `stars`
- `language`
- `product_category`

The primary key is arranged so the program can search by product category and star rating.

## JSON Data

The program asks the user to enter the JSON file name.

Example:

```text
Enter the JSON file name: dataset_en_dev.json
```

The program expects each JSON record to contain fields such as:

```json
{
    "review_id": "R12345",
    "product_id": "P100",
    "reviewer_id": "U200",
    "stars": 5,
    "review_body": "Great product.",
    "review_title": "Very Good",
    "language": "en",
    "product_category": "Books"
}
```

The data is inserted into both the `Reviews` and `ProductCategories` tables.

## CQL Commands Used

The application uses Cassandra Query Language commands including:

```sql
CREATE KEYSPACE
CREATE TABLE
INSERT
SELECT
SELECT COUNT(*)
ALTER TABLE
DROP TABLE
DROP KEYSPACE
```

## Example CQL SELECT Statements

The program allows the user to enter CQL `SELECT` commands, such as:

```sql
SELECT * FROM Amazon.Reviews;
```

or:

```sql
SELECT * FROM Amazon.ProductCategories;
```

## Verifying the Keyspace and Tables in cqlsh

Start `cqlsh`:

```bash
cqlsh
```

Display the keyspaces:

```sql
DESCRIBE KEYSPACES;
```

Switch to the Amazon keyspace:

```sql
USE Amazon;
```

The prompt should change to something similar to:

```text
cqlsh:amazon>
```

Display the tables:

```sql
DESCRIBE TABLES;
```

You should see:

```text
reviews
productcategories
```

## CRUD Operations

### Create

The program creates the keyspace and tables and inserts JSON records.

### Read

The program displays product categories, counts reviews by star rating, and allows CQL `SELECT` queries.

### Update

The program allows the user to alter the table structure by adding or removing columns.

### Delete

The program allows the user to delete tables and delete the Amazon keyspace.

## Important Notes

- Cassandra must be running before the Python program is started.
- Run the Python application from the normal Linux/Ubuntu terminal, not from inside `cqlsh`.
- `cqlsh` can be used to verify the keyspace, tables, and data.
- The JSON file name and location must be correct before importing data.
- Create the Amazon keyspace before creating the tables.
- Create both tables before importing the JSON data.

## Project Files

```text
Amazon_Cassandra_CRUD.py
README.md
JSON review dataset
```

## Conclusion

This project demonstrates the use of Python, the `cassandra-driver` library, and CQL commands to perform CRUD operations with Apache Cassandra. The menu allows the user to create database objects, import JSON data, retrieve review information, modify table columns, and delete Cassandra tables and keyspaces.
