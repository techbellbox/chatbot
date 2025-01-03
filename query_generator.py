def generate_sql_query(llm, prompt, max_tokens=200):
    """Generate a SQL query using the LLM."""
    try:
        output = llm(prompt, max_tokens=max_tokens)
        return output["choices"][0]["text"].strip()
    except Exception as e:
        print(f"Error generating SQL query: {e}")
        return None
