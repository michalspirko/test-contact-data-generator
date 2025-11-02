# Test Contact Data Generator

A flexible Python application for generating realistic test contact data with configurable output formats. Generate synthetic contact information for testing, development, and database population purposes.

## Features

- **Multiple Output Formats**: Export data to CSV files, MySQL, or PostgreSQL databases
- **Configurable Data Generation**: Control the probability of each field being populated
- **Realistic Data**: Uses the Faker library to generate authentic-looking contact information
- **Flexible Configuration**: INI-based configuration files for easy customization
- **Modular Architecture**: Clean, object-oriented design with separated concerns

## Generated Contact Fields

- First Name
- Last Name
- Date of Birth
- Email Address
- Phone Number
- Street Address (Line 1 & 2)
- City
- State/Province
- Postal Code
- Country

## Prerequisites

- Python 3.x
- pip (Python package manager)

### Required Python Packages

- `faker` - For generating fake data
- `mysql-connector-python` - For MySQL database connectivity (if using MySQL)
- `psycopg2` - For PostgreSQL database connectivity (if using PostgreSQL)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/test-contact-data-generator.git
cd test-contact-data-generator
```

2. Install required dependencies:
```bash
pip install faker mysql-connector-python psycopg2-binary
```

3. Create necessary directories:
```bash
mkdir csv_output
```

## Configuration

Configuration files are stored in INI format. Three sample configurations are provided:

### CSV Configuration (`config_csv.ini`)

```ini
[main]
db_type = csv
number_of_contacts = 10

[probabilities]
date_of_birth = 0.5
email = 0.5
phone = 0.5
...
```

### MySQL Configuration (`config_mysql.ini`)

```ini
[main]
db_type = mysql
number_of_contacts = 10

[database]
database = test_data
user = root
password = your_password
host = localhost
port = 3306

[probabilities]
...
```

### PostgreSQL Configuration (`config_postgresql.ini`)

```ini
[main]
db_type = postgresql
number_of_contacts = 10

[database]
database = test_data
user = postgres
password = your_password
host = localhost
port = 5432

[probabilities]
...
```

### Configuration Options

- **number_of_contacts**: Number of contact records to generate (positive integer)
- **probabilities**: Value between 0 and 1 for each field, controlling the likelihood of that field being populated (0 = never, 1 = always)

## Usage

Run the script with the path to your configuration file:

```bash
python DataGenerator.py <path_to_config_file>
```

### Examples

Generate CSV file:
```bash
python DataGenerator.py ./config_csv.ini
```

Generate data in MySQL database:
```bash
python DataGenerator.py ./config_mysql.ini
```

Generate data in PostgreSQL database:
```bash
python DataGenerator.py ./config_postgresql.ini
```

## Output

### CSV Output
CSV files are created in the `csv_output/` directory with timestamps:
- Format: `contact_data_YYYY-MM-DDTHH-MM-SS.csv`
- Delimiter: Semicolon (`;`)

### Database Output
For MySQL and PostgreSQL:
- Creates database if it doesn't exist
- Creates a new table with timestamp: `contact_data_YYYY_MM_DDTHH_MM_SS`
- Inserts all generated records into the table

## Project Structure

```
test-contact-data-generator/
├── DataGenerator.py              # Main entry point
├── utils/
│   ├── CommandValidator.py       # CLI argument validation
│   ├── ConfigLoader.py           # Configuration file parsing
│   └── ContactGenerator.py       # Contact data generation logic
├── writers/
│   ├── BaseWriter.py             # Abstract base class for writers
│   ├── CSVWriter.py              # CSV file writer
│   ├── MySQLWriter.py            # MySQL database writer
│   └── PostgreSQLWriter.py       # PostgreSQL database writer
├── config_csv.ini                # Sample CSV configuration
├── config_mysql.ini              # Sample MySQL configuration
├── config_postgresql.ini         # Sample PostgreSQL configuration
└── csv_output/                   # Output directory for CSV files
```

## Error Handling

The application includes comprehensive error handling for:
- Invalid command-line arguments
- Missing or malformed configuration files
- Invalid configuration values
- Database connection failures
- Missing database credentials
