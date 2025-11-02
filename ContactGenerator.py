from faker import Faker
import random


class ContactGenerator:
    """
    Class for generating contact data based on given probabilities.
    """

    def __init__(self, faker, probabilities):
        """
        Initialize ContactDataGenerator with a Faker instance and probabilities.

        Args:
            faker (Faker): A Faker instance used to generate the fake data.
            probabilities (dict): A dictionary containing the probability of generating
                                 each field in the contact data.
        """
        self.faker = faker
        self.probabilities = probabilities

    def generate_contact_data(self):
        """
        Generate contact data based on given probabilities.

        This method generates a dictionary containing fake contact data using the
        Faker library. Each field of the contact data is generated with the probability
        specified in the 'probabilities' dictionary.

        Returns:
            dict: A dictionary containing the generated contact data.
        """

        # Dictionary with contact data
        contact_data = {
            "first_name": self.faker.first_name()[:20],
            "last_name": self.faker.last_name()[:20],
            "date_of_birth": self.faker.date(pattern="%Y-%m-%d") if random.random() <= self.probabilities.get(
                "date_of_birth", 1) else None,
            "email": (
                self.faker.email() if "@" in self.faker.email() else "user@example.com") if random.random() <=
                                                                                            self.probabilities.get(
                                                                                                "email", 1) else None,
            "phone": ''.join(filter(str.isdigit, self.faker.phone_number()))[:10] if random.random() <=
                                                                                     self.probabilities.get("phone", 1)
            else None,
            "street_address_1": self.faker.street_address()[:40] if random.random() <= self.probabilities.get(
                "street_address_1", 1) else None,
            "street_address_2": self.faker.secondary_address()[:40] if random.random() <= self.probabilities.get(
                "street_address_2", 1) else None,
            "city": self.faker.city()[:40] if random.random() <= self.probabilities.get("city", 1) else None,
            "state_province": self.faker.state()[:20] if random.random() <= self.probabilities.get("state_province",
                                                                                                   1) else None,
            "postal_code": self.faker.zipcode()[:10] if random.random() <= self.probabilities.get("postal_code",
                                                                                                  1) else None,
            "country": self.faker.country()[:40] if random.random() <= self.probabilities.get("country", 1) else None
        }

        # Return the dictionary
        return contact_data
