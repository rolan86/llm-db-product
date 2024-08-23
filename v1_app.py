"""
Reference Material:
https://medium.com/@zuhayr.codes/query-your-postgresql-database-with-langchain-and-llama-3-1-exploring-llms-1-ba3a9560c0d1
"""

"""
Product VERSION 1 of the application or the MVP
This cli application can generate consume the SQLite database,
The database description is provided by us as a hardcoded entry
The question to the LLM is also hardcoded
"""


from langchain_community.llms import Ollama
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain


llm = Ollama(model="llama3")

sqlite_db_path = 'companies_in_germany_partial.db'
db = SQLDatabase.from_uri(f'sqlite:///{sqlite_db_path}')

db.get_usable_table_names()

chain = create_sql_query_chain(llm=llm, db=db)

database_description = (
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
response = chain.invoke({"question": database_description + "Give me all the companies have their headquarters are similar to Berlin?"})

print(response)
