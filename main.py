import asyncio

from dotenv import load_dotenv

from ToolAgent import ToolAgent
from Tools import get_tools

if __name__ == '__main__':
    load_dotenv(override=True)

    agent = ToolAgent(get_tools())

    asyncio.run(agent.arun())