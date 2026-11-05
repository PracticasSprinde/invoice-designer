from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.product_sch import Product as ProductSchema, ProductCreate
from app.repositories import products as products_repo
from tests.memory_storage import product_list, find_product

# Define ruta
router = APIRouter(prefix="/products", tags=["Products"])
router_memory = APIRouter(prefix="/memory/products", tags=["Products (memory)"])


# ================== CONSULTAS API ==================


# Añadir usuario
@router_memory.post("/", summary="Create a new product", status_code=status.HTTP_201_CREATED)
def create_product(product : ProductSchema):
    if find_product(product.product_id):
        raise HTTPException(
            status_code=409, 
            detail=f"Creation failed: product with ID {product.product_id} already exists."
        )
    
    product_list.append(product)
    return product


# Obtener todos los usuarios
@router_memory.get("/", summary="Get list of products")
def get_users():
    if not product_list:
        raise HTTPException(
            status_code=404, 
            detail="No registered products found."
        )
    
    return product_list


# Obtener usuario por ID
@router_memory.get("/{product_id}", summary="Get a product by ID")
def get_product(product_id:int):
    product = find_product(product_id)
   
    if product is None:
        raise HTTPException(
            status_code=404, 
            detail=f"No product found with ID {product_id}."
        )
    
    return product


# Modificar usuario
@router_memory.put("/{product_id}", summary="Update an existing product")
def update_product(product_id: int, product:ProductSchema):
    for index, saved in enumerate (product_list):
        if saved.product_id == product_id:
            product.product_id = product_id
            product_list[index] = product
            return product
    
    raise HTTPException(
        status_code=404, 
        detail=f"Update failed: product with ID {product_id} not found."
    )


# Eliminar usuario
@router_memory.delete("/{product_id}", summary="Delete a product", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    product = find_product(product_id)
    
    if product is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Deletion failed: product with ID {product_id} not found."
        )
    
    product_list.remove(product)


# ================== CONSULTAS BASE DATOS ==================


# Añadir usuario
@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    return products_repo.create_product(data, db)


# Obtener todos los usuarios
@router.get("/", response_model=list[ProductSchema], summary="Get list of product")
def list_products(db: Session = Depends(get_db)):
    return products_repo.list_products(db)


# Obtener usuario por ID
@router.get("/{product_id}", response_model= ProductSchema, summary="Get a product by ID")
def get_user(product_id: int, db: Session = Depends(get_db)):
    product = products_repo.get_user(product_id, db)
    
    if product is None:
        raise HTTPException(
            status_code=404, 
            detail=f"No product product with ID {product_id}."
        )
    
    return product


# Modificar usuario
@router.put("/{product_id}", response_model= ProductSchema, summary="Update an existing product")
def update_product(product_id: int, data: ProductCreate, db: Session = Depends(get_db)):
    product = products_repo.update_user(product_id, data, db)
    
    if product is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Update failed: product with ID {product_id} not found."
        )
    
    return product


# Eliminar usuario
@router.delete("/{product_id}", summary="Delete a product", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = products_repo.delete_user(product_id, db)
    
    if not product:
        raise HTTPException(
            status_code=404, 
            detail=f"Deletion failed: product with ID {product_id} not found."
        )