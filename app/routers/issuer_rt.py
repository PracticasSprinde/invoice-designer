from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.issuer_sch import Issuer as IssuerSchema, IssuerCreate
from app.repositories import issuer_repo as issuer_repo
from tests.memory_storage import issuers_list, find_issuer

# Define ruta
router = APIRouter(prefix="/issuer", tags=["Issuer"])
router_memory = APIRouter(prefix="/memory/issuer", tags=["Issuer (memory)"])


# ================== CONSULTAS API ==================


# Añadir usuario
@router_memory.post("/", summary="Create a new issuer", status_code=status.HTTP_201_CREATED)
def create_issuer(issuer : IssuerSchema):
    if find_issuer(issuer.issuer_id):
        raise HTTPException(
            status_code=409, 
            detail=f"Creation failed: issuer with ID {issuer.issuer_id} already exists."
        )
    
    issuers_list.append(issuer)
    return issuer


# Obtener todos los usuarios
@router_memory.get("/", summary="Get list of issuer")
def get_issuers():
    if not issuers_list:
        raise HTTPException(
            status_code=404, 
            detail="No registered issuer found."
        )
    
    return issuers_list


# Obtener usuario por ID
@router_memory.get("/{issuer_id}", summary="Get a issuer by ID")
def get_issuer(issuer_id:int):
    issuer = find_issuer(issuer_id)
   
    if issuer is None:
        raise HTTPException(
            status_code=404, 
            detail=f"No issuer found with ID {issuer_id}."
        )
    
    return issuer


# Modificar usuario
@router_memory.put("/{issuer_id}", summary="Update an existing issuer")
def update_issuer(issuer_id: int, issuer:IssuerSchema):
    for index, saved in enumerate (issuers_list):
        if saved.issuer_id == issuer_id:
            issuer.issuer_id = issuer_id
            issuers_list[index] = issuer
            return issuer
    
    raise HTTPException(
        status_code=404, 
        detail=f"Update failed: issuer with ID {issuer_id} not found."
    )


# Eliminar usuario
@router_memory.delete("/{issuer_id}", summary="Delete a issuer", status_code=status.HTTP_204_NO_CONTENT)
def delete_issuer(issuer_id: int):
    issuer = find_issuer(issuer_id)
    
    if issuer is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Deletion failed: issuer with ID {issuer_id} not found."
        )
    
    issuers_list.remove(issuer)


# ================== CONSULTAS BASE DATOS ==================


# Añadir usuario
@router.post("/", response_model=IssuerSchema, status_code=status.HTTP_201_CREATED)
def create_issuer(data: IssuerCreate, db: Session = Depends(get_db)):
    return issuer_repo.create_issuer(data, db)


# Obtener todos los usuarios
@router.get("/", response_model=list[IssuerSchema], summary="Get list of issuer")
def list_users(db: Session = Depends(get_db)):
    return issuer_repo.list_users(db)


# Obtener usuario por ID
@router.get("/{issuer_id}", response_model= IssuerSchema, summary="Get a issuer by ID")
def get_issuer(issuer_id: int, db: Session = Depends(get_db)):
    issuer = issuer_repo.get_issuer(issuer_id, db)
    
    if issuer is None:
        raise HTTPException(
            status_code=404, 
            detail=f"No issuer found with ID {issuer_id}."
        )
    
    return issuer


# Modificar usuario
@router.put("/{issuer_id}", response_model= IssuerSchema, summary="Update an existing issuer")
def update_issuer(issuer_id: int, data: IssuerCreate, db: Session = Depends(get_db)):
    issuer = issuer_repo.update_issuer(issuer_id, data, db)
    
    if issuer is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Update failed: issuer with ID {issuer_id} not found."
        )
    
    return issuer


# Eliminar usuario
@router.delete("/{issuer_id}", summary="Delete a issuer", status_code=status.HTTP_204_NO_CONTENT)
def delete_issuer(issuer_id: int, db: Session = Depends(get_db)):
    issuer = issuer_repo.delete_issuer(issuer_id, db)
    
    if not issuer:
        raise HTTPException(
            status_code=404, 
            detail=f"Deletion failed: issuer with ID {issuer_id} not found."
        )