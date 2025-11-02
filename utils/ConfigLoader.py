import configparser
import sys


class ConfigLoader:
    """
    Class for loading and validating the configuration file.
    """

    def __init__(self, config_file_path):
        """
        Initialize ConfigLoader with the path to the configuration file.

        Args:
            config_file_path (str): The path to the configuration file.
        """
        self.config_file_path = config_file_path

    def load_config(self):
        """
        Loads and validates the configuration file.

        This method reads the given configuration file and checks if the
        file exists, is in the correct format, and contains valid values for
        number_of_contacts, probabilities, and database connection data.

        Returns:
            tuple: A tuple containing the number_of_contacts, db_config, and probabilities.

        Raises:
            SystemExit: If the configuration file is not found, not in the correct format,
                        has invalid number_of_contacts, probabilities or missing required database keys.
        """

        # Validate if the file exists
        try:
            with open(self.config_file_path, 'r'):
                pass
        except FileNotFoundError:
            print(f"Error: Config file not found at {self.config_file_path}. Please check the file path.")
            sys.exit(1)

        # Instantiate ConfigParser
        config = configparser.ConfigParser()

        # Try reading the config file, validate if format is correct
        try:
            config.read(self.config_file_path)
        except configparser.Error as e:
            print(f"Error: Invalid INI format in config file - {e}")
            sys.exit(1)

        # Validate db_type
        db_type = config.get("main", "db_type")
        if db_type not in ("csv", "postgresql", "mysql"):
            print(f"Error: Invalid db_type specified in the config file. Must be: csv, postgresql or mysql.")
            sys.exit(1)

        # Validate number_of_contacts(int() - integer; number_of_contacts < 1 - positive integer)
        number_of_contacts_str = config.get("main", "number_of_contacts")

        if not number_of_contacts_str.isdigit() or int(number_of_contacts_str) < 1:
            print("Error: Invalid number_of_contacts specified in the config file. Must be a positive integer.")
            sys.exit(1)
        else:
            number_of_contacts = int(number_of_contacts_str)

        # Validate probabilities and save into dictionary
        probabilities = {}

        for key, value in config.items("probabilities"):
            # Validate if numeric
            try:
                value = float(value)
            except ValueError:
                print(f"Error: Invalid input for {key}. Must be a positive integer or a float between 0 and 1.")
                sys.exit(1)
            # Validate probability range
            if not (0 <= value <= 1):
                print(f"Error: Invalid probability value for {key}. Must be between 0 and 1.")
                sys.exit(1)
            else:
                probabilities[key] = value

        # Validate database connection data if config file is config_postgresql or config_mysql (all keys present)
        if config.has_section("database"):
            db_config = {
                key: value for key, value in config.items("database")
            }
            if db_type in ['postgresql', 'mysql']:
                required_keys = {"host", "port", "user", "password", "database"}

                missing_keys = required_keys - db_config.keys()
                if missing_keys:
                    print(
                        f"Error: Missing required keys in the 'database' section of the config file: "
                        f"{', '.join(missing_keys)}")
                    sys.exit(1)
        else:
            db_config = None

        # Return number of contacts, database configuration, probabilities
        return db_type, number_of_contacts, db_config, probabilities
