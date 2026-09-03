from app.database.connection import SessionLocal
from app.models import Product, Inventory
from sqlalchemy import func

def insert_products():
    db = SessionLocal()
    try:
        # Lista de produtos (SKU como chave para evitar duplicatas)
        products_data = [
            {"name": "Smartphone XYZ", "description": "Smartphone com 128GB, tela 6.5\"", "sku": "SM-001", "price": 1999.99},
            {"name": "Notebook ABC", "description": "Notebook 14\" 8GB RAM 256GB SSD", "sku": "NB-002", "price": 3499.99},
            {"name": "Fone Bluetooth", "description": "Fone de ouvido bluetooth com cancelamento de ruído", "sku": "FN-003", "price": 299.99},
            {"name": "Tablet 10\"", "description": "Tablet 10\" 64GB Wi-Fi", "sku": "TB-004", "price": 1599.99},
        ]

        for item in products_data:
            # Verifica se o produto já existe pelo SKU
            existing = db.query(Product).filter(Product.sku == item["sku"]).first()
            if existing:
                print(f"Produto '{item['name']}' (SKU: {item['sku']}) já existe. Pulando.")
                continue

            # Cria novo produto
            product = Product(
                name=item["name"],
                description=item["description"],
                sku=item["sku"],
                price=item["price"]
            )
            db.add(product)
            db.commit()
            db.refresh(product)

            # Estoque inicial (50 unidades)
            inventory = Inventory(product_id=product.id, quantity=50)
            db.add(inventory)
            db.commit()
            print(f"✅ Produto '{product.name}' inserido com sucesso!")

        print("\n🎯 Todos os produtos foram processados.")

    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    insert_products()