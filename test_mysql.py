from app.database.connection import SessionLocal
from app.models import Customer, Conversation, Message

def test_connection():
    db = SessionLocal()
    try:
        # Tenta contar quantos clientes existem
        count = db.query(Customer).count()
        print(f"Conexão OK! Existem {count} clientes no banco.")
        
        # Se quiser listar os primeiros clientes
        customers = db.query(Customer).limit(5).all()
        for c in customers:
            print(f"Cliente: {c.name} ({c.channel}) - {c.external_id}")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()