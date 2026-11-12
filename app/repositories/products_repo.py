from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.products_mdl import Product
from app.schemas.products_sch import ProductCreate


# Añadir producto en la base de datos
def create_product(data: ProductCreate, db: Session) -> Product:

    # Buscar el último código del usuario
    products = db.scalars(
        select(Product)
        .where(Product.user_id == data.user_id)
        .order_by(Product.product_id.desc())
    ).all()

    # Calcular el siguiente número
    next_number = 1

    for existing_product in products:

        if existing_product.code and existing_product.code.startswith("PROD-"):

            try:
                number = int(existing_product.code.replace("PROD-", ""))

                if number >= next_number:
                    next_number = number + 1

            except ValueError:
                continue

    # Genera el código automáticamente
    code = "PROD-" + str(next_number).zfill(3)

    # Crea el producto
    product_data = data.model_dump()
    product_data["code"] = code

    product = Product(**product_data)

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
    for field, value in data.model_dump(exclude={"code"}).items():
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
