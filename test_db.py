
from sqlalchemy import text
from app.core.database import engine

try:
    with engine.connect() as connection:
        resultado = connection.execute(text("SELECT VERSION()"))
        version = resultado.fetchone()

        print("Conexión correcta con MySQL")
        print("Versión de MySQL:", version[0])

except Exception as error:
    print("Error al conectar con MySQL:", error)
