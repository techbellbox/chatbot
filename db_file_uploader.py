from db_connector import connect_to_db
import csv

# Connect to MySQL server
conn = connect_to_db
cursor = conn.cursor()

# 1. Create the VoterDetails table
create_table_query = """
CREATE TABLE IF NOT EXISTS VoterDetails (
    voter_id INT AUTO_INCREMENT PRIMARY KEY,
    voter_name VARCHAR(255),
    mobile_number VARCHAR(20),
    constituency VARCHAR(255),
    gender VARCHAR(50),
    marital_status VARCHAR(50),
    education_qualification VARCHAR(255),
    schemes TEXT
);
"""

cursor.execute(create_table_query)
print("Table 'VoterDetails' created successfully!")

# 2. Upload CSV contents into the VoterDetails table
csv_file_path = './Synthetic_Voter_Data_with_Schemes.csv'  # Replace with the path to your CSV file

# Open and read the CSV file
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)  # Using DictReader to read as dictionary

    # Insert each row into the VoterDetails table
    for row in csvreader:
        # Safely access columns with .get() to avoid KeyError
        voter_name = row.get('Voter Name', 'N/A')
        mobile_number = row.get('Mobile Number', 'N/A')
        constituency = row.get('Constituency', 'N/A')
        gender = row.get('Gender', 'N/A')
        marital_status = row.get('Marital Status', 'N/A')
        education_qualification = row.get('Education Qualification', 'N/A')
        schemes = row.get('Schemes', 'N/A')
        
        # Insert the data into the table
        cursor.execute("""
        INSERT INTO VoterDetails (voter_name, mobile_number, constituency, gender, marital_status, education_qualification, schemes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (voter_name, mobile_number, constituency, gender, marital_status, education_qualification, schemes))


    # Commit the changes to the database
    conn.commit()
    print(f"Successfully uploaded CSV to VoterDetails table!")

# Close the cursor and connection
cursor.close()
conn.close()
