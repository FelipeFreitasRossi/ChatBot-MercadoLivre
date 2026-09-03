#!/usr/bin/env python
from app.database.connection import engine, Base
from app.models import Customer, Conversation, Message

def create_tables():
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    create_tables()