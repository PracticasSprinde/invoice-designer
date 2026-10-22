from decimal import Decimal
from types import SimpleNamespace

from app.services.calculations import calculate_subtotal, calculate_discount, calculate_tax, round_money, calculate_invoice_totals

# Crear líneas de prueba
lines = [
    SimpleNamespace(quantity=Decimal("2"), unit_price=Decimal("10"), tax_rate=Decimal(21)),
    SimpleNamespace(quantity=Decimal("3"), unit_price=Decimal("5"), tax_rate=Decimal(21))
]

discount_percent = Decimal("10")

# Probar el método de subtotal
subtotal = calculate_subtotal(lines)
print("Subtotal:", subtotal)

# Probar el método de calcular el porcentaje de subtotal
discount = calculate_discount(subtotal,discount_percent) # 10 % de descuento
print("discount:", discount)

# Probar calcular iva
tax = calculate_tax(lines, discount_percent)
print ("IVA:", tax)

# Redondear decimales
decimales = round_money(tax)
print ("Redondeo:", decimales)

# Total factura
total_factura = calculate_invoice_totals(lines, discount_percent)
print("Total Factura:", total_factura)