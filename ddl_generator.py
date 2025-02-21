import csv
import os


def generate_ddl(csv_file_path, table_name, ddl_output_dir, primary_key_column=None):
    """
    Generates a DDL (Data Definition Language) SQL script to create a table
    based on the headers of a CSV file.

    Args:
        csv_file_path: Path to the CSV file.
        table_name: The desired name for the SQL table.
        ddl_output_dir: Directory to store the generated DDL file.
        primary_key_column: (Optional) The name of the column to be used as the primary key.  If None, no primary key is defined in this function (you can add it manually to the generated script).  If a column name is given, and it exists, it will be used.  If the column name doesn't exist, there will be no primary key.
    Returns:
        ddl_file_path or None: The full path to the generated DDL file, or None if an error occurs.
    """
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Get the header row

            # Create the DDL statement
            ddl_statement = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"

            column_definitions = []
            for column_name in header:
                # Basic type inference (you can customize this)
                # Check if the column can be an integer
                is_integer = True
                csvfile.seek(0)  # Reset file pointer to the beginning
                next(csv.reader(csvfile)) #skip the header row
                for row in csv.reader(csvfile):
                  try:
                    if row[header.index(column_name)].strip() != "": #allow for null/empty values
                      int(row[header.index(column_name)])
                  except (ValueError, IndexError):
                    is_integer = False
                    break  # No need to check further if one value is not an integer
                
                # Check if column might be a float
                is_float = True
                csvfile.seek(0)
                next(csv.reader(csvfile)) #skip header
                for row in csv.reader(csvfile):
                    try:
                        if row[header.index(column_name)].strip() != "":
                            float(row[header.index(column_name)])
                    except (ValueError, IndexError):
                        is_float = False
                        break

                if is_integer:
                    column_type = "INT"
                elif is_float:
                    column_type = "FLOAT"  # Or DECIMAL, depending on precision needs
                else:
                    column_type = "VARCHAR(255)"  # Default to VARCHAR

                col_def = f"    {column_name} {column_type}"

                # Add primary key constraint if specified and column exists
                if primary_key_column and primary_key_column == column_name:
                    col_def += " PRIMARY KEY"

                column_definitions.append(col_def)

            ddl_statement += ",\n".join(column_definitions)
            ddl_statement += "\n);"

            # Create the output directory if it doesn't exist
            os.makedirs(ddl_output_dir, exist_ok=True)

            # Write the DDL statement to a file
            ddl_file_path = os.path.join(ddl_output_dir, f"{table_name}_ddl.sql")
            with open(ddl_file_path, 'w', encoding='utf-8') as ddl_file:
                ddl_file.write(ddl_statement)
            return ddl_file_path

    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def main():
    # --- Configuration ---
    csv_file_path = './data/csv/Synthetic_Voter_Data_with_Schemes.csv'  # Path to your CSV
    table_name = 'VoterDetails'  # The table name you want to use
    ddl_output_dir = './data/ddl'  # Folder to store the DDL file
    primary_key_column = '' 

    # --- Generate DDL ---
    ddl_file = generate_ddl(csv_file_path, table_name, ddl_output_dir, primary_key_column)
    if ddl_file:
        print(f"DDL file generated and saved to: {ddl_file}")


if __name__ == "__main__":
    main()
