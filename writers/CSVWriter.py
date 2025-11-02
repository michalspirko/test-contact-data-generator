import csv
from datetime import datetime
from .BaseWriter import BaseWriter


class CSVWriter(BaseWriter):
    """
    Class for generating contact data and writing it to a CSV file.
    """

    # Initialize without unnecessary db_config parameter
    def __init__(self, number_of_contacts, contact_generator):
        super().__init__(number_of_contacts, None, contact_generator)

    def write(self):
        """
        Generate contact data and write it to a CSV file.

        This method generates contact data for a specified number of contacts using the Faker library
        and the given probabilities. The generated data is then written to a CSV file with a timestamp
        in its name.

        Returns:
            None
        """

        # Generate a timestamp for the CSV file name
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

        # Open a new CSV file for writing
        with open(f'csv_output/contact_data_{timestamp}.csv', 'w', newline='') as csvfile:
            # Create a CSV writer object
            csv_writer = csv.writer(csvfile, delimiter=';')

            # Define the header for the CSV file
            header = ['first_name', 'last_name', 'date_of_birth', 'email', 'phone', 'street_address_1',
                      'treet_address_2', 'city', 'state_province', 'postal_code', 'country']

            # Write the header to the CSV file
            csv_writer.writerow(header)

            # Generate and write data for the specified number of contacts
            for i in range(self.number_of_contacts):
                # Generate contact data and format it as a list, then write it to the CSV file
                row = [*self.contact_generator.generate_contact_data().values()]
                csv_writer.writerow(row)

        # Print a success message with the name of the created CSV file
        print(f"CSV created successfully: contact_data_{timestamp}.csv")

