from dotenv import load_dotenv
load_dotenv()

#we will need - db, llm, tools, create_agent, memory, system prompt


#----------------------------DB Created-------------------------------

from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///task_mngmnt.db")

db.run("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT CHECK (
            status IN ('pending', 'completed', 'in_progress')
        ) DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

# print("DB Created Successfully")

#----------------------------LLM Creation-------------------------

from langchain_groq import ChatGroq
from langchain.agents import create_agent

llm = ChatGroq(
    model = "openai/gpt-oss-120b",
    temperature=0,
    streaming=True
)

#-----------------------toolkit--------------------------
from langchain_community.agent_toolkits import SQLDatabaseToolkit

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()

# for tool in tools:
#     print(tool.name)

#o/p = sql_db_query
#      sql_db_schema
#      sql_db_list_tables
#      sql_db_query_checker

#------------------------------memory---------------------------


from langgraph.checkpoint.memory import InMemorySaver
memory = InMemorySaver()


#-------------------------------system Prompt---------------------------

system_prompt = """
You are a task management assistant that interacts with a SQL database containing a 'tasks' table. 

TASK RULES:
1. Limit SELECT queries to 10 results max with ORDER BY created_at DESC
2. After CREATE/UPDATE/DELETE, confirm with SELECT query
3. Correct grammaar and formatting fof given task and description before adding to rhe table.
4. If the user requests a list of tasks, present the output in a structured table format to ensure a clean and organized display in the browser."

CRUD OPERATIONS:
    CREATE: INSERT INTO tasks(title, description, status)
    READ: SELECT * FROM tasks WHERE ... LIMIT 10
    UPDATE: UPDATE tasks SET status=? WHERE id=? OR title=?
    DELETE: DELETE FROM tasks WHERE id=? OR title=?

Table schema: id, title, description, status(pending/in_progress/completed), created_at.
"""

#-----------------------------agent creation----------------------------

from langchain.agents import create_agent
# agent = create_agent(
#     model = llm,
#     tools = tools,
#     checkpointer = memory,
#     system_prompt = system_prompt
# )

# while True:
#     query = input("User: ")
#     res = agent.invoke({"messages":[{"role":"user","content":query}]},{"configurable":{"thread_id":"2"}})
#     print("AI: ",res["messages"][-1].content)
    
#-----------------------------------web Interface----------------------------
import streamlit as st

@st.cache_resource                           #it will not let streamlit reinitialize agent and memory again and again
def get_agent():
    agent = create_agent(
        model = llm,
        tools = tools,
        checkpointer = InMemorySaver(),
        system_prompt = system_prompt
    )
    return agent
agent = get_agent()

st.subheader("SQL based TO-DO Bot")
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])


prompt = st.chat_input("Ask to manage ur daily tasks!!!")
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role":"user","content":prompt})

    with st.chat_message("ai"):
        with st.spinner("Thinking..."):
            res = agent.invoke({"messages":[{"role":"user","content":prompt}]},{"configurable":{"thread_id":"2"}})
            st.markdown(res["messages"][-1].content)
            st.session_state.messages.append({"role":"ai","content":res["messages"][-1].content})
    


