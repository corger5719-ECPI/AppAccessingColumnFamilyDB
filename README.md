# AppAccessingColumnFamilyDB
3.5 Performance Assessment


# Cassandra Amazon Review Database Application

## Project Overview

This Python application demonstrates how to perform CRUD-related operations using an Apache Cassandra database. The program connects to Cassandra using the `cassandra-driver` Python library and provides a menu that allows the user to create database structures, import JSON data, perform queries, modify tables, and delete Cassandra tables or the keyspace.

The application uses an Amazon review dataset stored in JSON format.

## Program Requirements

The program uses:

* Python
* Apache Cassandra
* `cassandra-driver`
* JSON data file
* Cassandra Query Language (CQL)

## Database Structure

The application creates a Cassandra keyspace named:

`Amazon`

### Reviews Table

The `Reviews` table contains the following fields:

* `review_id`
* `product_id`
* `reviewer_id`
* `stars`
* `review_body`
* `review_title`
* `product_category`

### ProductCategories Table

The `ProductCategories` table contains the following fields:

* `product_id`
* `stars`
* `language`
* `product_category`

## Features

The application provides the following features:

1. Create the `Amazon` keyspace.
2. Create the `Reviews` table.
3. Create the `ProductCategories` table.
4. Read data from a JSON file and insert the data into both Cassandra tables.
5. Display all distinct product categories.
6. Display the number of reviews with 4 stars or higher for a product category entered by the user.
7. Display the number of 1-star reviews for a product category entered by the user.
8. Allow the user to enter and execute CQL `SELECT` statements.
9. Allow the user to add columns to the `Reviews` or `ProductCategories` tables.
10. Allow the user to remove columns from the `Reviews` or `ProductCategories` tables.
11. Delete the `Reviews` or `ProductCategories` table.
12. Delete the `Amazon` keyspace.
13. Exit the application.

## Installation

Python and Cassandra must be installed and Cassandra must be running before the application is started.

Install the Cassandra Python driver with:



Python Application Using CRUD Operations on a Cassandra Database
