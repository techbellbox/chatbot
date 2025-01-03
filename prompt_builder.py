def load_file_content(filepath):
    """Load content from a file."""
    try:
        with open(filepath, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return ""

def build_prompt(user_input, db_schema_file, query_examples_file):
    """Build a prompt for generating SQL queries."""
    db_schema = load_file_content(db_schema_file)
    query_examples = load_file_content(query_examples_file)

    return f"""
    Database Schema:
    {db_schema}

    Example Queries:
    {query_examples}

    User Request: {user_input}

    Generate a SQL query to fulfill the user's request. Only the sql query is needed, nothing else is required. Do not insert any format specifiers or backticks.
    """
