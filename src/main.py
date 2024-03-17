from argparse import ArgumentParser
from tool import get_columns, generate_cleaning_code
from langchain_openai import ChatOpenAI
from agent import Agent
from pprint import pprint


parser = ArgumentParser()
parser.add_argument("--query", type=str, required=True)


def main():
    arg = parser.parse_args()
    llm = ChatOpenAI(
        model="gpt-4-0125-preview",
        temperature=0,
    ) # Add your openai api key here
    tools = [get_columns, generate_cleaning_code]
    agent = Agent(llm=llm, tools=tools)
    response = agent.create_code(arg.query)
    pprint(response)


if __name__ == "__main__":
    main()
