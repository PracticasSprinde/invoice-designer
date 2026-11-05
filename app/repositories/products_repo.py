from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.products_mdl import Product
from app.schemas.product_sch import ProductCreate


# Añadir producto en la base de datos
def create_product(data: ProductCreate, db: Session) -> Product:
    # Crear plantilla
    product = Product(**data.model_dump())

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


# Retorna todos los productos
def list_products(db: Session) -> list[Product]:
    return list(db.scalars(select(Product)).all())


# Retorna producto por ID
def get_product(product_id: int, db: Session) -> Product | None:
    return db.get(Product, product_id)


# Modificar producto
def update_product(
    product_id: int, data: ProductCreate, db: Session
) -> Product | None:
    product = get_product(product_id, db)

    if product is None:
        return None

    # Actualiza datos
    for field, value in data.model_dump().items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


# Eliminar producto de la base de datos
def delete_product(product_id: int, db: Session) -> bool:
    product = get_product(product_id, db)

    if not product:
        return False

    db.delete(product)
    db.commit()
    return True
