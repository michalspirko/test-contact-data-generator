import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime
from .BaseWriter import BaseWriter


class PostgreSQLWriter(BaseWriter):
    """
    Class for generating contact data and writing it to a PostgreSQL database.
    """

    def write(self):
        """
        Write generated contact data to a PostgreSQL database.

        This method creates a new database if it doesn't exist, then creates a new table with a unique timestamp in
        the name, and inserts the generated contact data into that table. It connects to the PostgreSQL server using the
        provided db_config dictionary.

        Returns:
            None

        Raises:
            psycopg2.Error: If there is a problem with the database connection or queries.
        """
        # Connect to the default 'postgres' database
        try:
            default_db_config = self.db_config.copy()
            default_db_config["database"] = "postgres"

            connection = psycopg2.connect(**default_db_config)
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = connection.cursor()
        except psycopg2.DatabaseError as e:
            print(
                "Error: Unable to establish a connection to the PostgreSQL server. Please verify connection parameters.")
            print("Error details:", e)
            sys.exit(1)

        # Check if the target database exists and create it if it doesn't
        target_database = self.db_config["database"]
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{target_database}'")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f"CREATE DATABASE {target_database}")

        # Close the cursor and the connection to the 'postgres' database
        cursor.close()
        connection.close()

        # Connect to the target database
        connection = psycopg2.connect(**self.db_config)
        cursor = connection.cursor()

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
        connection.commit()

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
