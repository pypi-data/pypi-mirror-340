# rdsclient

 is a Python package designed to simplify the interaction with AWS RDS instances using the  package. It allows executing SQL queries and fetching the results as Pandas or Spark DataFrames.

## Features

- **Singleton RDS connection**: Ensures a single connection to the RDS instance.
- **Query execution**: Execute SELECT, INSERT, UPDATE, DELETE queries on your RDS database.
- **Return data as Pandas DataFrame**: Fetch query results directly as Pandas DataFrames for easy data manipulation.
- **Spark DataFrame support**: Optionally convert query results to Spark DataFrames for distributed computing.
- **Context-managed MySQL connection**: Automatically manage the connection lifecycle with Python's .

## Installation

You can install  directly from PyPI:

```bash
pip install rdsclient
```

### Prerequisites

- **Python 3.7+**
- **Dependencies**:
  - 
  - 
  - 

These dependencies are automatically installed when you install .

## Usage

### Simple Query Example

```python
from rdsclient import query_rds

# Define your RDS connection details
host = 'your-rds-host'
user = 'your-username'
password = 'your-password'
database = 'your-database'

# Execute the query and get the result as a Pandas DataFrame
df = query_rds(
    query='SELECT * FROM your_table',
    host=host,
    user=user,
    password=password,
    database=database
)

# Display the result
print(df.head())
```

### Using the RDS Class Directly

```python
from rdsclient import RDS

# Create an RDS instance
rds = RDS(
    host='your-rds-host',
    user='your-username',
    password='your-password',
    database='your-database'
)

# Execute a query and fetch results as a Pandas DataFrame
df = rds.execute_query('SELECT * FROM your_table')

# Optionally, get the results as a Spark DataFrame
spark_df = rds.query_to_spark_df('SELECT * FROM your_table')

# Display the Pandas DataFrame
print(df.head())
```

### Executing Non-Select Queries

You can also execute non-SELECT queries (such as INSERT, UPDATE, DELETE):

```python
# Example for executing an UPDATE query
affected_rows = rds.execute_update('UPDATE your_table SET column_name = %s WHERE condition = %s', ('new_value', 'condition_value'))

print(f'{affected_rows} rows affected.')
```

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please feel free to open an issue or submit a pull request.

### Steps for Contributing:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a new pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
