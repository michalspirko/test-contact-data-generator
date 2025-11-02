import mysql.connector
from datetime import datetime
import sys
from .BaseWriter import BaseWriter


class MySQLWriter(BaseWriter):
    """
    Class for writing contact data to a MySQL database.
    """

    def write(self):
        """
        Write generated contact data to a MySQL database.

        This function connects to the MySQL server using the provided db_config dictionary, creates a new database if
        it doesn't exist, then creates a new table with a unique timestamp in the name, and inserts the generated
        contact data into that table.

        Returns:
            None

        Raises:
            mysql.connector.Error: If there is a problem with the database connection or queries.
        """
        try:
            connect_config = self.db_config.copy()
            database_name = connect_config.pop('database')

            # Connect to MySQL without specifying the database
            connection = mysql.connector.connect(**connect_config)
            cursor = connection.cursor()
        except mysql.connector.DatabaseError as e:
            print("Error: Unable to establish a connection to the MySQL server. Please verify your connection parameters.")
            print("Error details:", e)
            sys.exit(1)

        # Create database if it doesn't exist
        create_database_query = f"CREATE DATABASE IF NOT EXISTS {database_name}"
        cursor.execute(create_database_query)

        # Use the specified database
        cursor.execute(f"USE {database_name}")

        # Create table with dynamic name
        timestamp = datetime.now().strftime("%Y_%m_%dT%H_%M_%S")
        table_name = f"contact_data_{timestamp}"
        create_table_query = f"""
            CREATE TABLE {table_name} (
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                date_of_birth DATE,
                email VARCHAR(255),
                phone VARCHAR(255),
                street_address_1 VARCHAR(255),
                street_address_2 VARCHAR(255),
                city VARCHAR(255),
                state_province VARCHAR(255),
                postal_code VARCHAR(255),
                country VARCHAR(255)
            );
        """

        cursor.execute(create_table_query)

        # Insert data into the table
        for i in range(self.number_of_contacts):
            contact_data = self.contact_generator.generate_contact_data()
            insert_query = f"""
                INSERT INTO {table_name} (first_name, last_name, date_of_birth, email, phone, street_address_1, 
                street_address_2, city, state_province, postal_code, country)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(insert_query, tuple(contact_data.values()))

        connection.commit()

        # Close the cursor and the connection
        cursor.close()
        connection.close()

        # Print a success message with table name
        print(f"Data inserted successfully into table: {table_name}")
