import csv
from db_connector import connect_to_db
import re

def create_table_from_csv(csv_file_path):
    # Connect to MySQL server
    conn = connect_to_db()
    cursor = conn.cursor()

    # Open and read the CSV file to fetch the column names
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)  # Using DictReader to read as dictionary
        fieldnames = csvreader.fieldnames  # Get the CSV column headers

    # Ensure that the column names are valid MySQL field names (no spaces, etc.)
    table_name = re.sub(r'\W|^(?=\d)', '_', csv_file_path.split('/')[-1].split('.')[0])  # Table name based on CSV file name

    # Dynamically create the table creation query based on CSV headers
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
    
    for column in fieldnames:
        # Create a safe column name (strip spaces, special characters)
        column_name = re.sub(r'\W|^(?=\d)', '_', column)
        create_table_query += f"    {column_name} VARCHAR(255),\n"

    # Remove the last comma and add the closing parenthesis
    create_table_query = create_table_query.rstrip(',\n') + "\n);"

    # Execute the table creation query
    cursor.execute(create_table_query)
    print(f"Table '{table_name}' created successfully!")

    # Insert data into the newly created table
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            # Prepare the column names and values for insertion
            columns = ', '.join([re.sub(r'\W|^(?=\d)', '_', col) for col in fieldnames])
            values = ', '.join([f"'{row.get(col, '')}'" for col in fieldnames])

            # Insert query
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            cursor.execute(insert_query)

        # Commit the changes to the database
        conn.commit()
        print(f"Successfully uploaded CSV to '{table_name}' table!")

    # Close the cursor and connection
    cursor.close()
    conn.close()
