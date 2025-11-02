import sys

from faker import Faker

from utils.CommandValidator import CommandValidator
from utils.ConfigLoader import ConfigLoader
from utils.ContactGenerator import ContactGenerator
from writers.CSVWriter import CSVWriter
from writers.MySQLWriter import MySQLWriter
from writers.PostgreSQLWriter import PostgreSQLWriter


def writer_factory(db_type, number_of_contacts, db_config, contact_generator):
    """
    Factory function to instantiate the correct writer class based on the 'db_type' parameter.

    Args:
        db_type (str): The type of the database. Either 'csv', 'mysql', or 'postgresql'.
        number_of_contacts (int): The number of contacts for which data should be generated.
        db_config (dict): A dictionary containing database connection parameters.
        contact_generator (ContactDataGenerator): An instance of ContactDataGenerator to generate fake data.

    Returns:
        An instance of the appropriate writer class.
    """
    if db_type == 'csv':
        return CSVWriter(number_of_contacts, contact_generator)
    elif db_type == 'postgresql':
        return PostgreSQLWriter(number_of_contacts, db_config, contact_generator)
    elif db_type == 'mysql':
        return MySQLWriter(number_of_contacts, db_config, contact_generator)
    else:
        raise ValueError("Invalid 'db_type' value. Must be 'csv', 'mysql', or 'postgresql'.")


def main():
    # Validate command line arguments and store path to configuration file
    command_validator = CommandValidator(sys.argv)
    config_file_path = command_validator.validate_cli_arguments()

    # Load and validate configuration file
    config_loader = ConfigLoader(config_file_path)
    db_type, number_of_contacts, db_config, probabilities = config_loader.load_config()

    # Instantiate ContactGenerator
    faker = Faker()
    contact_generator = ContactGenerator(faker, probabilities)

    # Instantiate writer object and write the data
    writer = writer_factory(db_type, number_of_contacts, db_config, contact_generator)
    writer.write()


# Calling the main function
if __name__ == "__main__":
    main()
