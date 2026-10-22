from decimal import Decimal

#Funciones de calculos para las facturas

# Calcular el subtotal
def calculate_subtotal(lines):

    subtotal = Decimal("0")
    
    for line in lines:
        subtotal += line.quantity * line.unit_price

    return subtotal
