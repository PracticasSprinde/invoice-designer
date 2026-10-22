from decimal import Decimal
from types import SimpleNamespace

from app.services.calculations import calculate_subtotal

# Crear líneas de prueba
lines = [
    SimpleNamespace(quantity=Decimal("2"), unit_price=Decimal("10")),
    SimpleNamespace(quantity=Decimal("3"), unit_price=Decimal("5"))
]

# Probar el método
subtotal = calculate_subtotal(lines)

print("Subtotal:", subtotal)