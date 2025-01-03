import os
from llama_cpp import Llama
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

def load_llm_model():
    """Load the Llama model with parameters from the .env file."""
    model_path = os.getenv("MODEL_PATH")
    n_threads = int(os.getenv("MODEL_THREADS", 8))
    n_batch = int(os.getenv("MODEL_BATCH", 1024))
    
    return Llama(model_path=model_path, n_threads=n_threads, n_batch=n_batch)


def generate_question(llm, prompt, max_tokens=200):
    """Generate a question using the provided LLM and prompt."""
    output = llm(prompt, max_tokens=max_tokens)
    response_text = output["choices"][0]["text"]
    return response_text

def generate_sql_query(llm, prompt, max_tokens=200, model_type="llama"):
    """Generate a SQL query using the provided LLM and prompt."""
    if model_type == "llama":
        output = llm(prompt, max_tokens=max_tokens)
        response_text = output["choices"][0]["text"]
    elif model_type == "openai":
        response = openai.ChatCompletion.create(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            messages=[{"role": "system", "content": "You are an SQL expert. Generate SQL queries based on user instructions."},
                      {"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        response_text = response["choices"][0]["message"]["content"]
    else:
        raise ValueError("Invalid model_type. Use 'llama' or 'openai'.")
    return response_text.strip()

def load_openai_api():
    """Set up OpenAI API credentials."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
