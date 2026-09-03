from app.database.connection import engine, Base
from app.models import Customer, Conversation, Message  # importa para registrar

def main():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    main()