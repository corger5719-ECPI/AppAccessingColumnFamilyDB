"""
Cora Germany
August 16, 2026
Assignment: Cassandra CRUD Application
Purpose: Create a Python application that uses CQL commands and the
cassandra-driver library to create, read, alter, and delete data and
database objects in an Amazon keyspace.
"""

import json
from cassandra.cluster import Cluster
from cassandra import InvalidRequest

# ---------------------------------------------------------
# Connect to the Cassandra server.
# The Python driver provides the connection. CQL statements
# are used for all Cassandra operations in this program.
# ---------------------------------------------------------
cluster = Cluster(["127.0.0.1"])
session = cluster.connect()


# ---------------------------------------------------------
# * Create a new keyspace named Amazon.
# ---------------------------------------------------------
def create_keyspace():
    cql = """
    CREATE KEYSPACE IF NOT EXISTS Amazon
    WITH replication = {
        'class': 'SimpleStrategy',
        'replication_factor': 1
    }
    """

    session.execute(cql)
    print("\nAmazon keyspace created successfully.")


# ---------------------------------------------------------
# * Create the Reviews table.
# ---------------------------------------------------------
def create_reviews_table():
    cql = """
    CREATE TABLE IF NOT EXISTS Amazon.Reviews (
        review_id text PRIMARY KEY,
        product_id text,
        reviewer_id text,
        stars int,
        review_body text,
        review_title text,
        product_category text
    )
    """

    try:
        session.execute(cql)
        print("\nReviews table created successfully.")
    except InvalidRequest:
        print("\nCreate the Amazon keyspace first.")


# ---------------------------------------------------------
# * Create the ProductCategories table.
#
# product_category is the partition key and stars is the
# first clustering column. This allows the required category
# and star-rating SELECT statements.
# ---------------------------------------------------------
def create_product_categories_table():
    cql = """
    CREATE TABLE IF NOT EXISTS Amazon.ProductCategories (
        product_id text,
        stars int,
        language text,
        product_category text,
        PRIMARY KEY ((product_category), stars, product_id)
    )
    """

    try:
        session.execute(cql)
        print("\nProductCategories table created successfully.")
    except InvalidRequest:
        print("\nCreate the Amazon keyspace first.")


# ---------------------------------------------------------
# * Insert data from the JSON file into the Reviews and
# ProductCategories tables.
# ---------------------------------------------------------
def insert_json_data():
    filename = input("\nEnter the JSON file name: ").strip()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            count = 0

            # This works with a JSON-lines file where each line
            # contains one JSON review object.
            for line in file:
                line = line.strip()

                if line == "":
                    continue

                review = json.loads(line)

                review_id = str(review.get("review_id", ""))
                product_id = str(review.get("product_id", ""))
                reviewer_id = str(review.get("reviewer_id", ""))
                stars = int(review.get("stars", 0))
                review_body = str(review.get("review_body", ""))
                review_title = str(review.get("review_title", ""))
                language = str(review.get("language", ""))
                product_category = str(review.get("product_category", ""))

                # CQL INSERT for the Reviews table.
                reviews_cql = """
                INSERT INTO Amazon.Reviews
                (review_id, product_id, reviewer_id, stars,
                 review_body, review_title, product_category)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

                session.execute(
                    reviews_cql,
                    (
                        review_id,
                        product_id,
                        reviewer_id,
                        stars,
                        review_body,
                        review_title,
                        product_category
                    )
                )

                # CQL INSERT for the ProductCategories table.
                categories_cql = """
                INSERT INTO Amazon.ProductCategories
                (product_id, stars, language, product_category)
                VALUES (%s, %s, %s, %s)
                """

                session.execute(
                    categories_cql,
                    (
                        product_id,
                        stars,
                        language,
                        product_category
                    )
                )

                count += 1

        print("\n" + str(count) + " records inserted.")

    except FileNotFoundError:
        print("\nFile not found. Check the file name and location.")
    except json.JSONDecodeError:
        print("\nThe JSON file contains invalid JSON.")
    except InvalidRequest as error:
        print("\nCassandra error:", error)
        print("Make sure the Amazon keyspace and both tables exist first.")
    except ValueError:
        print("\nA stars value in the JSON file could not be converted to an integer.")


# ---------------------------------------------------------
# * Display all distinct product categories from the
# ProductCategories table.
# ---------------------------------------------------------
def display_product_categories():
    cql = """
    SELECT DISTINCT product_category
    FROM Amazon.ProductCategories
    """

    try:
        rows = session.execute(cql)

        print("\nDISTINCT PRODUCT CATEGORIES")
        print("---------------------------")

        for row in rows:
            print(row.product_category)

    except InvalidRequest as error:
        print("\nCassandra error:", error)


# ---------------------------------------------------------
# * Display the count of reviews with 4 stars or higher for
# a product category entered by the user.
# ---------------------------------------------------------
def count_four_star_reviews():
    category = input("\nEnter a product category: ").strip()

    cql = """
    SELECT COUNT(*)
    FROM Amazon.ProductCategories
    WHERE product_category = %s
    AND stars >= 4
    """

    try:
        row = session.execute(cql, (category,)).one()

        print(
            "\nNumber of 4-star and higher reviews for "
            + category
            + ": "
            + str(row.count)
        )

    except InvalidRequest as error:
        print("\nCassandra error:", error)


# ---------------------------------------------------------
# * Display the count of 1-star reviews for a product
# category entered by the user.
# ---------------------------------------------------------
def count_one_star_reviews():
    category = input("\nEnter a product category: ").strip()

    cql = """
    SELECT COUNT(*)
    FROM Amazon.ProductCategories
    WHERE product_category = %s
    AND stars = 1
    """

    try:
        row = session.execute(cql, (category,)).one()

        print(
            "\nNumber of 1-star reviews for "
            + category
            + ": "
            + str(row.count)
        )

    except InvalidRequest as error:
        print("\nCassandra error:", error)


# ---------------------------------------------------------
# * Allow the user to type and execute a CQL SELECT
# statement.
# ---------------------------------------------------------
def execute_select_statement():
    print("\nExample:")
    print("SELECT * FROM Amazon.Reviews;")

    cql = input("\nEnter a CQL SELECT statement: ").strip()

    # This menu option is only for SELECT statements.
    if not cql.upper().startswith("SELECT"):
        print("\nOnly SELECT statements are allowed here.")
        return

    try:
        rows = session.execute(cql)

        print("\nQUERY RESULTS")
        print("-------------")

        found = False

        for row in rows:
            found = True
            print(row)

        if not found:
            print("No records found.")

    except Exception as error:
        print("\nCQL error:", error)


# ---------------------------------------------------------
# Ask the user which required table they want to change.
# ---------------------------------------------------------
def choose_table():
    print("\n1. Reviews")
    print("2. ProductCategories")

    choice = input("Choose a table: ").strip()

    if choice == "1":
        return "Amazon.Reviews"
    elif choice == "2":
        return "Amazon.ProductCategories"
    else:
        print("\nInvalid table choice.")
        return None


# ---------------------------------------------------------
# Make sure a column name contains only letters, numbers,
# and underscores before placing it in a CQL command.
# ---------------------------------------------------------
def valid_column_name(name):
    if name == "":
        return False

    return name.replace("_", "").isalnum()


# ---------------------------------------------------------
# * Allow the user to add a column to the Reviews or
# ProductCategories table.
# ---------------------------------------------------------
def add_column():
    table = choose_table()

    if table is None:
        return

    column_name = input("\nEnter the new column name: ").strip()

    if not valid_column_name(column_name):
        print("\nInvalid column name.")
        return

    print("\nCommon Cassandra data types:")
    print("text, int, bigint, boolean, decimal, timestamp")

    data_type = input("Enter the Cassandra data type: ").strip().lower()

    allowed_types = [
        "text",
        "int",
        "bigint",
        "boolean",
        "decimal",
        "timestamp"
    ]

    if data_type not in allowed_types:
        print("\nInvalid data type.")
        return

    # CQL ALTER TABLE ... ADD command.
    cql = (
        "ALTER TABLE "
        + table
        + " ADD "
        + column_name
        + " "
        + data_type
    )

    try:
        session.execute(cql)
        print("\nColumn added successfully.")
    except Exception as error:
        print("\nCQL error:", error)


# ---------------------------------------------------------
# * Allow the user to remove a column from the Reviews or
# ProductCategories table.
# ---------------------------------------------------------
def remove_column():
    table = choose_table()

    if table is None:
        return

    column_name = input("\nEnter the column name to remove: ").strip()

    if not valid_column_name(column_name):
        print("\nInvalid column name.")
        return

    # CQL ALTER TABLE ... DROP command.
    cql = "ALTER TABLE " + table + " DROP " + column_name

    try:
        session.execute(cql)
        print("\nColumn removed successfully.")
    except Exception as error:
        print("\nCQL error:", error)


# ---------------------------------------------------------
# * Allow the user to delete the Reviews or
# ProductCategories table.
# ---------------------------------------------------------
def delete_table():
    table = choose_table()

    if table is None:
        return

    confirm = input(
        "\nType YES to delete " + table + ": "
    ).strip().upper()

    if confirm == "YES":
        # CQL DROP TABLE command.
        cql = "DROP TABLE IF EXISTS " + table

        try:
            session.execute(cql)
            print("\nTable deleted successfully.")
        except Exception as error:
            print("\nCQL error:", error)
    else:
        print("\nTable was not deleted.")


# ---------------------------------------------------------
# * Allow the user to delete the Amazon keyspace.
# ---------------------------------------------------------
def delete_keyspace():
    confirm = input(
        "\nType YES to delete the Amazon keyspace: "
    ).strip().upper()

    if confirm == "YES":
        # CQL DROP KEYSPACE command.
        cql = "DROP KEYSPACE IF EXISTS Amazon"

        try:
            session.execute(cql)
            print("\nAmazon keyspace deleted successfully.")
        except Exception as error:
            print("\nCQL error:", error)
    else:
        print("\nAmazon keyspace was not deleted.")


# ---------------------------------------------------------
# Main menu
# ---------------------------------------------------------
def main_menu():
    while True:
        print("\n==========================================")
        print("       AMAZON CASSANDRA MENU")
        print("==========================================")
        print("1. Create Amazon keyspace")
        print("2. Create Reviews table")
        print("3. Create ProductCategories table")
        print("4. Insert data from JSON file")
        print("5. Display distinct product categories")
        print("6. Count 4-star and higher reviews")
        print("7. Count 1-star reviews")
        print("8. Execute a CQL SELECT statement")
        print("9. Add a column")
        print("10. Remove a column")
        print("11. Delete a table")
        print("12. Delete Amazon keyspace")
        print("13. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            create_keyspace()
        elif choice == "2":
            create_reviews_table()
        elif choice == "3":
            create_product_categories_table()
        elif choice == "4":
            insert_json_data()
        elif choice == "5":
            display_product_categories()
        elif choice == "6":
            count_four_star_reviews()
        elif choice == "7":
            count_one_star_reviews()
        elif choice == "8":
            execute_select_statement()
        elif choice == "9":
            add_column()
        elif choice == "10":
            remove_column()
        elif choice == "11":
            delete_table()
        elif choice == "12":
            delete_keyspace()
        elif choice == "13":
            print("\nProgram ended.")
            break
        else:
            print("\nInvalid choice. Please try again.")


# ---------------------------------------------------------
# Start the application.
# ---------------------------------------------------------
try:
    main_menu()
finally:
    cluster.shutdown()
