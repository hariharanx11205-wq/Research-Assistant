import os
import operator
from typing import Annotated, List, TypedDict, Union

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# --- Tools ---
search_tool = DuckDuckGoSearchRun()

# --- State ---
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

# --- Nodes ---

def call_model(state: AgentState):
    """
    Decides whether to use a tool or answer directly.
    """
    messages = state["messages"]
    
    # Initialize the LLM with OpenRouter config
    llm = ChatOpenAI(
        model="openai/gpt-3.5-turbo", # Or any other supported model on OpenRouter
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
        streaming=True
    )
    
    # Bind tools to the LLM (if model supports function calling, otherwise we might need a react style agent)
    # For simplicity and broad compatibility with OpenRouter models, we'll use a ReAct-style prompt or tool binding if supported.
    # Let's try standard tool binding first, as many OpenRouter models support it.
    llm_with_tools = llm.bind_tools([search_tool])
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def call_tool(state: AgentState):
    """
    Executes the tool call.
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    # Parsing tool calls
    tool_calls = last_message.tool_calls
    
    results = []
    for t in tool_calls:
        if t["name"] == "duckduckgo_search":
            print(f"Searching for: {t['args']}")
            res = search_tool.invoke(t["args"])
            results.append(
                {"tool_call_id": t["id"], "name": t["name"], "content": res}
            )
            
    # We return the tool outputs as ToolMessages (LangChain expects raw tool outputs to be converted, 
    # but here we can just append them if using standard structure or use ToolMessage)
    from langchain_core.messages import ToolMessage
    
    tool_messages = [
        ToolMessage(tool_call_id=res["tool_call_id"], content=res["content"], name=res["name"])
        for res in results
    ]
    
    return {"messages": tool_messages}

# --- Conditional Logic ---

def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

# --- Graph Construction ---

workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", call_tool)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

workflow.add_edge("tools", "agent")

app = workflow.compile()

if __name__ == "__main__":
    # Test
    inputs = {"messages": [HumanMessage(content="What is the current stock price of Google?")]}
    result = app.invoke(inputs)
    print(result["messages"][-1].content)
