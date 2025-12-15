import os
from sqlmodel import SQLModel, create_engine, Session, select
from .models import Pizza

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/pizzabot")

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        statement = select(Pizza)
        results = session.exec(statement).first()
        
        if not results:
            pizzas = [
                Pizza(name="Calabresa", ingredients="Molho de tomate, queijo, calabresa", price=40.00),
                Pizza(name="Mussarela", ingredients="Molho de tomate, queijo, orégano", price=35.00),
                Pizza(name="Portuguesa", ingredients="Molho de tomate, queijo, presunto, ovo, cebola, azeitona", price=45.00),
                Pizza(name="Frango com Catupiry", ingredients="Molho de tomate, queijo, frango desfiado, catupiry", price=42.00),
            ]
            session.add_all(pizzas)
            session.commit()
