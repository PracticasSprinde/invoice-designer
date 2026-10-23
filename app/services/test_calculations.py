from decimal import Decimal
from types import SimpleNamespace

from app.services.calculations import calculate_line, calculate_discount, round_money, calculate_invoice_totals

# Crear líneas de prueba
lines = [
    SimpleNamespace(quantity=Decimal("2"), unit_price=Decimal("10"), discount_percent= Decimal("20"), tax_rate=Decimal("21")),
    SimpleNamespace(quantity=Decimal("3"), unit_price=Decimal("5"), discount_percent= Decimal("10"), tax_rate=Decimal("21"))
]

global_discount_percent = Decimal("10")

# # Probar el método de subtotal
# subtotal = calculate_subtotal(lines)
# print("Subtotal:", subtotal)

# # Probar el método de calcular el porcentaje de subtotal
# discount = calculate_discount(subtotal,discount_percent) # 10 % de descuento
# print("discount:", discount)

# # Probar calcular iva
# tax = calculate_tax(lines, discount_percent)
# print ("IVA:", tax)

# # Redondear decimales
# decimales = round_money(tax)
# print ("Redondeo:", decimales)


# Prueba 1: Importe total de la linea
line = SimpleNamespace(
    quantity=Decimal("1"),
    unit_price=Decimal("100"),
    discount_percent=Decimal("10"),
    tax_rate=Decimal("21"),
)
total_linea = calculate_line(line, global_discount_percent)
print("Prueba 2: Total de la linea:", total_linea)

# Prueba 2: descuento solo de línea (20 %) y global a 0
line_3 = SimpleNamespace(
    quantity=Decimal("1"),
    unit_price=Decimal("100"),
    discount_percent=Decimal("20"),
    tax_rate=Decimal("21"),
)
print("Prueba 3: Solo descuento de línea:", calculate_line(line_3, Decimal("0")))

# Prueba 13: Importe total de la factura
total_factura = calculate_invoice_totals(lines, global_discount_percent)
print("Prueba 1: Factura completa:", total_factura)
