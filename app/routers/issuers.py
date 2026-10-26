from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

# Define ruta
router = APIRouter(prefix="/issuers", tags=["Issuers"])

# -----------------------------CLASES-----------------------------

# Entidad
class Issuer(BaseModel):
    issuer_id: int
    name: str
    last_name: str
    email: str
    enterprise: str
    cif_nif: str
    phone: str


# -----------------------------ATRIBUTOS Y METODOS-----------------------------

issuer_list = [
    Issuer(issuer_id=1, name="Paco", last_name="Saez", email= "aaa@gmail.com",enterprise="Google", cif_nif="B075673", phone="666666666"),
    Issuer(issuer_id=2, name="Sara", last_name="Alonso",email= "aaa@gmail.com", enterprise="Prisma", cif_nif="B0533567", phone="444444444"),
    Issuer(issuer_id=3, name="Laura", last_name="Pascual",email= "aaa@gmail.com", enterprise="Pallicer", cif_nif="B85373", phone="777777777"),
    Issuer(issuer_id=4, name="Sergio", last_name="Perez",email= "aaa@gmail.com", enterprise="Toyota", cif_nif="B88337", phone="699999999")
]

# Devuelve el primer emisor que coincida con el ID
def find_issuer(issuer_id: int) -> Issuer | None:
    return next((i for i in issuer_list if i.issuer_id == issuer_id), None)


# -----------------------------ENDPOINTS-----------------------------

# Obtener todos los emisores
@router.get("/")
def all_issuers():
    if not issuer_list:
        raise HTTPException(status_code=404, detail="No se ha encontrado el emisor")
    return issuer_list

# Obtener emisor por ID
@router.get("/{issuer_id}")
def get_issuer(issuer_id:int):
    issuer = find_issuer(issuer_id)
    if issuer is None:
        raise HTTPException(status_code=404, detail="No hay ningún emisor con el id proporcionado")
    return issuer

# Añadir emisor
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_issuer(issuer : Issuer):
    if find_issuer(issuer.issuer_id):
        raise HTTPException(status_code=409, detail="No se ha podido añadir el emisor")
    issuer_list.append(issuer)
    return issuer

# Modificar emisor
@router.put("/{issuer_id}")
def update_issuer(issuer_id: int, issuer:Issuer):
    for index, saved in enumerate(issuer_list):
        if saved.issuer_id == issuer.issuer_id:
            issuer_list[index] = issuer
            return issuer
    raise HTTPException(status_code=404, detail="No se ha podido modificar el emisor")

# Eliminar emisor
@router.delete("/{issuer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issuer(issuer_id: int):
    issuer = find_issuer(issuer_id)
    if issuer is None:
        raise HTTPException(status_code=404, detail="Emisor no encontrado")
    issuer_list.remove(issuer)