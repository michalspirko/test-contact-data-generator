import sys


class CommandValidator:
    """
    Class for validating configuration file path and command line arguments.
    """

    def __init__(self, arguments):
        """
        Initialize ConfigValidator with command line arguments.
        Arguments:
            arguments (list[str]): List of command line arguments.
        """
        self.arguments = arguments

    def validate_cli_arguments(self):
        """
        Validate command line arguments and return the configuration file path.

        This method checks if the correct number of arguments are provided. If any validation fails, the program
        will exit with an error message. If validation passes, the method returns the configuration file path.

        Returns:
            str: The path to the configuration file if the command line arguments are valid.

        Raises:
            SystemExit: If the command line arguments are invalid the program will exit with a non-zero status.
        """
        # Validate correct usage of the command
        if len(self.arguments) != 2:
            print("Error: Invalid command. Follow usage: python <script_file_path> <config_file_path>\n"
                  "Example Command: python .\DataGenerator.py .\configs\config_mysql.ini")
            sys.exit(1)

        # Assigning file path of the config file
        config_file_path = self.arguments[1]

        # Return path to configuration file
        return config_file_path
