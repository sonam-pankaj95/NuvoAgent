from fastapi import FastAPI
from src.tool import get_columns, generate_cleaning_code
from langchain_openai import ChatOpenAI
from src.agent import Agent

app = FastAPI()

llm = ChatOpenAI(model = "gpt-4-0125-preview", temperature = 0)

cleaning_tools = [get_columns, generate_cleaning_code]
cleaning_agent = Agent(llm=llm, tools = cleaning_tools)

@app.post("/create_code")
async def create_code(query: str):
    return cleaning_agent.create_code(query)