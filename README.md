# SQL-Based To-Do Bot 🤖

A smart, AI-powered To-Do list application built with **Streamlit** and **LangChain**. Instead of manually clicking around to manage your tasks, you can simply chat with the bot to create, read, update, or delete your daily tasks!

## Features 🚀
- **Natural Language Task Management**: Just tell the bot what to do (e.g., "Add a task to buy groceries" or "Mark my project task as in_progress").
- **SQLite Database**: All tasks are stored securely in a local `task_mngmnt.db` file.
- **Powered by Groq**: Fast and accurate LLM responses using `ChatGroq`.
- **Interactive UI**: Clean and simple chat interface built with Streamlit.

## Tech Stack 🛠️
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend/AI**: [LangChain](https://python.langchain.com/) & [LangGraph](https://langchain-ai.github.io/langgraph/)
- **Database**: SQLite
- **LLM Provider**: Groq

## How to Run 🏃‍♂️

1. Ensure you have your API keys set up in a `.env` file (e.g., `GROQ_API_KEY`).
2. Install the required dependencies:
   ```bash
   pip install streamlit langchain langchain-groq langchain-community langgraph python-dotenv
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
4. Start chatting with your new AI assistant to manage your day!
