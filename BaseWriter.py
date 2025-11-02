from abc import ABC, abstractmethod


class BaseWriter(ABC):
    """
    Abstract Base Class representing a writer.
    """

    def __init__(self, number_of_contacts, db_config, contact_generator):
        """
        Initialize BaseWriter with the number of contacts and a ContactDataGenerator instance.

        Args:
            number_of_contacts (int): The number of contacts for which data should be generated.
            db_config (dict): Dictionary with database connection details
            contact_generator (ContactDataGenerator): An instance of ContactDataGenerator to generate fake data.
        """
        self.number_of_contacts = number_of_contacts
        self.db_config = db_config
        self.contact_generator = contact_generator

    @abstractmethod
    def write(self):
        """
        Write generated contact data to a specific output.

        This method needs to be implemented in every child class.

        Returns:
            None
        """
        pass
