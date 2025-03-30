import os

from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.graph import MessagesState
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode

from Tools import get_tools

def save_graph(graph: CompiledStateGraph):
    image = graph.get_graph().draw_mermaid_png()
    save_path = os.getenv("GRAPH_STATE_SAVE_PATH")

    # Save image to path
    with open(save_path, "wb") as image_file:
        image_file.write(image)

    print("Graph saved to {}".format(save_path))

def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

class ToolAgent:
    def __init__(self, tools):
        model_name = os.getenv("MODEL_NAME")
        llm = ChatOllama(model=model_name)

        self.print_debug_msg = bool(os.getenv("PRINT_DEBUG_MSG"))
        self.llm_with_tools = llm.bind_tools(get_tools())
        self.tool_node = ToolNode(tools)

    def __call_model(self, state: MessagesState):
        messages = state["messages"]
        response = self.llm_with_tools.invoke(messages)

        return {"messages": [response]}

    def run(self):
        workflow = StateGraph(MessagesState)

        # Define the two nodes we will cycle between
        workflow.add_node("agent", self.__call_model)
        workflow.add_node("tools", self.tool_node)

        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", should_continue, ["tools", END])
        workflow.add_edge("tools", "agent")

        graph = workflow.compile()

        if self.print_debug_msg:
            save_graph(graph)

        while True:
            query = input("What you want to query?: ")
            message = {"messages": [("human", query)]}

            for chunk in graph.stream(message, stream_mode="values"):
                chunk["messages"][-1].pretty_print()