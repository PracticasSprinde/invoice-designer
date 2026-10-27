
from sqlalchemy import text
from app.core.database import engine

from app.core.database import DATABASE_URL

print("URL utilizada:", DATABASE_URL.split("@")[-1])

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))
        print("Conexión correcta con PostgreSQL")
        print(result.scalar())

except Exception as error:
    print("Error al conectar con PostgreSQL:")
    print(error)

finally:
    engine.dispose()
