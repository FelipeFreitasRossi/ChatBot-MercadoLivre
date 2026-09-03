from sqlalchemy.orm import Session
from app.models import Product, Inventory

class ProductService:
    @staticmethod
    def find_product_by_name(db: Session, query: str) -> list[dict]:
        """Busca produtos cujo nome contenha a query (case-insensitive)."""
        products = db.query(Product).filter(Product.name.ilike(f"%{query}%")).all()
        result = []
        for p in products:
            inventory = db.query(Inventory).filter(Inventory.product_id == p.id).first()
            stock = inventory.quantity if inventory else 0
            result.append({
                "id": p.id,
                "name": p.name,
                "price": float(p.price) if p.price else None,
                "stock": stock,
                "description": p.description
            })
        return result

    @staticmethod
    def get_product_by_sku(db: Session, sku: str) -> dict | None:
        product = db.query(Product).filter(Product.sku == sku).first()
        if not product:
            return None
        inventory = db.query(Inventory).filter(Inventory.product_id == product.id).first()
        return {
            "id": product.id,
            "name": product.name,
            "price": float(product.price) if product.price else None,
            "stock": inventory.quantity if inventory else 0,
            "description": product.description
        }