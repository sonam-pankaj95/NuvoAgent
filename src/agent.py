from langchain.agents import initialize_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import AgentType

class Agent:
    def __init__(self, tools, llm):
        self.llm = llm
        self.tools = tools
        self.conversational_memory = ConversationBufferWindowMemory(
            memory_key="chat_history", k=5, return_messages=True
        )

        self.agent = initialize_agent(
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            tools=self.tools,
            llm=self.llm,
            verbose=True,
            max_iterations=3,
            early_stopping_method="generate",
            memory=self.conversational_memory,
        )

    def create_code(self, prompt):
        response = self.agent(
            f"get the list of columns from crm_demo.xlsx and then pass all the columns to the cleaning_function along with the following actions to perform: {prompt} Output just the code without any explanations"
        )
        return response['output']
