import os
import pprint

from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

class ToolAgent:
    def __init__(self, tools):
        model_name = os.getenv("MODEL_NAME")

        print(tools)

        self.tools = tools
        self.llm = ChatOllama(model=model_name)
        self.print_debug_msg = bool(os.getenv("PRINT_DEBUG_MSG"))

        tool_names = ", ".join(tool.name for tool in tools)
        system_message = f"You are a helpful assistant. Make sure to use the following tools for information: {tool_names}."

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )

    async def arun(self):
        agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)

        # Create an agent executor by passing in the agent and tools
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

        while True:
            query = input("What you want to query?: ")

            chunks = []

            async for chunk in agent_executor.astream({"input": query}):
                chunks.append(chunk)
                print("------")
                pprint.pprint(chunk, depth=1)