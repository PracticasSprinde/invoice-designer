from decimal import Decimal, ROUND_HALF_UP



#Funciones de calculos para las facturas


# Calcula los importes de una linea:
#   - line_amount: Cantidad * precio, aplicando el descuento de esa linea
#   - tax_amount: IVA correspondiente a esa linea
#
# El descuento global no modifica el importe de la línea que se muestra,
# pero se aplica al calcular el IVA de la factura.o.
#
# Orden: descuento de línea -> descuento global -> IVA.
def calculate_line(line, global_discount_percent):
    gross = line.quantity * line.unit_price # Importe bruto
    line_discount = calculate_discount(gross, global_discount_percent) # Euros de descuento de linea
    line_amount = gross - line_discount # Mostrado como "Importe"
    global_discount = calculate_discount(line_amount, global_discount_percent) #Euros de descuento global
    taxable = line_amount - global_discount # Base para el IVA
    tax_amount = taxable * line.tax_rate / Decimal("100") # Cantidad IVA en euros
    return round_money(line_amount), round_money(tax_amount)


# Calcula el subtotal sumando los importes de todas las líneas de la factura
def calculate_subtotal(lines):
    subtotal = Decimal("0") # Acumulador
    
    for line in lines:
        subtotal += line.quantity * line.unit_price # Añade el importe de cada línea
    return subtotal


# Calcular el descuento del subtotal (cuantos € se descuentan)
def calculate_discount(subtotal, discount_percent):
    discount = subtotal * discount_percent / Decimal("100") # discount_percent almacena el % de descuento que se aplica
    return discount


# Calcula el IVA total de la factura (en euros).
# Calcula línea a línea (cada línea puede tener un tipo de IVA distinto)
# El IVA se calcula despues de aplicar el descuento
def calculate_tax(lines, discount_percent):

    tax = Decimal("0") # Acumulador

    for line in lines:
        line_amount = line.quantity * line.unit_price # Importe de la línea sin descuento: cantidad x precio unitario
        discount = calculate_discount(line_amount, discount_percent) # Euros que se descuentan de esta línea
        discounted_amount = line_amount - discount # Importe de la línea con el descuento aplicado
        tax_line = discounted_amount * line.tax_rate / Decimal("100")  # IVA de esta línea
        tax += tax_line # Sumamos IVA de esta línea al total
    return tax


# Redondear una cantidad a dos decimales hacia arriba
def round_money(amount):
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)



# Callcula los importes tottales de una factura
def calculate_invoice_totals(lines, discount_percent):
    subtotal = calculate_subtotal(lines) 
    discount_amount = calculate_discount(subtotal, discount_percent)
    tax_amount = calculate_tax(lines, discount_percent)
    total = subtotal - discount_amount + tax_amount
    return{ # Importes redondeados
        "subtotal": round_money(subtotal),
        "discount_amount": round_money(discount_amount),
        "tax_amount": round_money(tax_amount),
        "total": round_money(total)
    }
