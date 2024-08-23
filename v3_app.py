"""
Product VERSION 3 of the application
This cli application can generate consume the SQLite database,
The database description is provided by us as a hardcoded entry
The question to the LLM is also hardcoded
We have extended the application to a feature to execute the SQL query returned by the LLM
But, we have modularized the code for ease of readability and extending the application to more features
"""


import sqlite3
from langchain_community.llms import Ollama
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain

def create_llm():
    """
    Initialize the LLM (Large Language Model) using Ollama.
    """
    return Ollama(model="llama3")

def setup_database(sqlite_db_path):
    """
    Set up the connection to the SQLite database using SQLDatabase utility.
    """
    return SQLDatabase.from_uri(f'sqlite:///{sqlite_db_path}')

def describe_database():
    """
    Return a description of the database structure for the LLM prompt.
    """
    return (
        "The database consists of one table: `companies`. This is a sqlite database, so you need to use sqlite-related queries.\n\n"
        "Reply only with the SQL query and nothing else, that includes any suggestions or comments.\n\n"
        "The `companies` table records details about the various companies in Germany. It includes the following columns:\n"
        "- `company_name`: Name of the company\n"
        "- `website`: The company website\n"
        "- `founded`: The year when the company was founded.\n"
        "- `industry`: The industry type that the company belongs to.\n"
        "- `headquarters`: The headquarters location for the company in Germany\n\n"
        "- `number_of_employees`: The number of employees in the company."
    )

def generate_sql_query(chain, description, question):
    """
    Generate the SQL query using the LLM chain.
    """
    response = chain.invoke({"question": description + question})
    return response

def execute_sql_query(connection, sql_query):
    """
    Execute the SQL query on the SQLite database and return the results.
    """
    cursor = connection.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()
    return results

def main():
    """
    Main function to run the entire process.
    """
    # Set up the LLM and database
    llm = create_llm()
    sqlite_db_path = 'companies_in_germany_partial.db'
    db = setup_database(sqlite_db_path)
    
    # Check usable table names (optional, can be used for validation or debugging)
    db.get_usable_table_names()
    
    # Create the query chain
    chain = create_sql_query_chain(llm=llm, db=db)
    
    # Describe the database and generate the SQL query
    database_description = describe_database()
    question = "Give me all the companies have their headquarters are similar to Berlin?"
    sql_query = generate_sql_query(chain, database_description, question)
    
    print(f"Generated SQL Query: {sql_query}")
    print("********")
    
    # Execute the SQL query and fetch results
    connection = sqlite3.connect(sqlite_db_path)
    results = execute_sql_query(connection, sql_query)
    
    # Print the results
    for row in results:
        print(row)
    
    # Close the database connection
    connection.close()

if __name__ == "__main__":
    main()

