import os
import operator
from typing import Annotated, List, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_groq import ChatGroq
from langchain_core.messages import AnyMessage, SystemMessage
from .tools import get_pizza_price, get_full_menu

class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]
    cart: List[str]
    total: float

tools = [get_pizza_price, get_full_menu]

llm = ChatGroq(
    temperature=0, 
    model_name="openai/gpt-oss-120b", 
    api_key=os.getenv("GROQ_API_KEY")
)
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = """Você é um assistente virtual da 'Pizza Bot', uma pizzaria delivery.
Seu objetivo é ajudar o cliente a escolher pizzas e fazer pedidos.
Você tem acesso ao cardápio completo através da ferramenta 'get_full_menu' e preços individuais através da ferramenta 'get_pizza_price'.
Sempre verifique o preço no banco de dados antes de informar ao cliente.
Quando o cliente confirmar um item, confirme o valor e o total do pedido.
Se o cliente finalizar, mostre o resumo.
"""

def chatbot(state: AgentState):
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

graph_builder = StateGraph(AgentState)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools))

graph_builder.set_entry_point("chatbot")

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
from langgraph.checkpoint.memory import MemorySaver

graph_builder.add_edge("tools", "chatbot")

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
