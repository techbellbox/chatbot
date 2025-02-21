import streamlit as st
from llm_model import load_openai_api, generate_sql_query
from db_connector import connect_to_db, execute_sql_query
from prompt_builder import build_prompt
import pandas as pd
import os
from ddl_generator import generate_ddl
from csv_uploader import create_table_from_csv

@st.cache_resource(ttl=3600)
def setup_connection():
    """Set up the environment and initialize OpenAI API."""
    load_openai_api()

def main():
    setup_connection()

    # Add Sidebar with Navigation
    st.sidebar.title("Navigation")
    selected_section = st.sidebar.radio("Go to:", ["Chatbot", "Upload Dataset"])

    if selected_section == "Chatbot":
        render_chatbot()
    elif selected_section == "Upload Dataset":
        render_dataset_upload()

def render_chatbot():
    """Render the chatbot interface."""
    st.title("💬 Text-to-SQL Chatbot")
    st.caption("🚀 A chatbot that converts natural language to SQL queries!")

    # Initialize chat messages in session state if not already set
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Ask me a question, and I'll generate a SQL query!"}
        ]

    # Display chat messages
    for message in st.session_state.messages:
        avatar = "⭐" if message["role"] == "assistant" else "🐼"
        with st.chat_message(message["role"], avatar=avatar):
            st.write(message["content"])

    # Input field for user
    if prompt := st.chat_input("Your question"):
        # Append user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Immediately display the user's message
        with st.chat_message("user", avatar="🐼"):
            st.write(prompt)

        # Generate SQL query using LLM
        with st.spinner("Generating SQL query..."):
            try:
                llm_prompt = build_prompt(prompt, "data/ddl/voter_details.sql", "data/queries/voter_details.sql")
                sql_query = generate_sql_query(None, llm_prompt, model_type="openai")
                
                # Append assistant's response to the session state
                st.session_state.messages.append({"role": "assistant", "content": sql_query})

                # Display the SQL query
                with st.chat_message("assistant", avatar="⭐"):
                    st.write("Here is the generated SQL query:")
                    st.code(sql_query, language="sql")

                # Execute the SQL query and display results
                with connect_to_db() as conn:
                    result = execute_sql_query(conn, sql_query)
                st.write("Query Results:")
                st.dataframe(result)

            except Exception as e:
                error_message = f"Error: {e}"
                st.session_state.messages.append({"role": "assistant", "content": error_message})
                with st.chat_message("assistant", avatar="⭐"):
                    st.error(error_message)

# Define the folder path where uploaded datasets will be stored
UPLOAD_FOLDER = "./data/csv/"

# Ensure the folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def render_dataset_upload():
    """Render the dataset upload section with a sub-section for viewing uploaded datasets."""
    st.title("📂 Upload Dataset")
    st.caption("Upload a dataset to view or process it.")

    # Initialize session state for datasets
    if "uploaded_datasets" not in st.session_state:
        st.session_state.uploaded_datasets = {}

    # File uploader
    uploaded_file = st.file_uploader("Upload your dataset (CSV, XLSX)", type=["csv", "xlsx"])

    # Automatically set a flag to indicate that a file has been uploaded
    if uploaded_file:
        try:
            # Save uploaded file to local folder
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Load dataset
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(file_path)

            # Save dataset in session state
            st.session_state.uploaded_datasets[uploaded_file.name] = df

            # Display confirmation
            st.success(f"Dataset '{uploaded_file.name}' uploaded and saved locally!")

        except Exception as e:
            st.error(f"Error loading dataset: {e}")

    # Sub-section for viewing datasets (both local and uploaded)
    st.subheader("View Datasets")
    
    # Get all local datasets in the upload folder
    existing_datasets = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith((".csv", ".xlsx"))]

    # Merge existing datasets with session datasets, removing duplicates
    all_datasets = existing_datasets + list(st.session_state.uploaded_datasets.keys())

    # Ensure no duplicates are shown
    all_datasets = list(set(all_datasets))

    if all_datasets:
        # Auto-select the newly uploaded dataset if there is one
        selected_dataset = st.selectbox(
            "Select a dataset to view:", 
            all_datasets, 
            index=len(all_datasets) - 1 if uploaded_file else 0  # Auto-select the newly uploaded dataset
        )

        if selected_dataset:
            # Check if the dataset is from the uploaded files in session state
            if selected_dataset in st.session_state.uploaded_datasets:
                df_selected = st.session_state.uploaded_datasets[selected_dataset]
            else:
                # If not, load it from the local folder
                file_path = os.path.join(UPLOAD_FOLDER, selected_dataset)
                if selected_dataset.endswith(".csv"):
                    df_selected = pd.read_csv(file_path)
                elif selected_dataset.endswith(".xlsx"):
                    df_selected = pd.read_excel(file_path)

            st.write(f"Preview of '{selected_dataset}':")
            st.dataframe(df_selected)

            # Provide download option for the selected dataset
            st.download_button(
                label=f"Download '{selected_dataset}' as CSV",
                data=df_selected.to_csv(index=False),
                file_name=selected_dataset,
                mime="text/csv"
            )
    else:
        st.info("No datasets found. Please upload a dataset to view it.")

if __name__ == "__main__":
    main()
