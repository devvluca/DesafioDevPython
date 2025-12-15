from langchain_core.tools import tool
from sqlmodel import Session, select
from .database import engine
from .models import Pizza

@tool
def get_pizza_price(pizza_name: str) -> str:
    with Session(engine) as session:
        statement = select(Pizza).where(Pizza.name == pizza_name)
        pizza = session.exec(statement).first()
        
        if not pizza:
            statement = select(Pizza).where(Pizza.name.ilike(f"%{pizza_name}%"))
            pizza = session.exec(statement).first()

        if pizza:
            return f"A pizza de {pizza.name} custa R$ {pizza.price:.2f} e leva {pizza.ingredients}."
        else:
            return f"Desculpe, não encontrei a pizza '{pizza_name}' no cardápio."

@tool
def get_full_menu() -> str:
    with Session(engine) as session:
        statement = select(Pizza)
        pizzas = session.exec(statement).all()
        
        if not pizzas:
            return "O cardápio está vazio no momento."
        
        menu = "| Pizza | Preço | Ingredientes |\n|-------|-------|--------------|\n"
        for pizza in pizzas:
            menu += f"| {pizza.name} | R$ {pizza.price:.2f} | {pizza.ingredients} |\n"
        
        return menu
