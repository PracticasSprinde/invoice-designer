from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
HUNDRED = Decimal("100")


# Redondear una cantidad a dos decimales hacia arriba
def round_money(amount):
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


# Calcular el descuento del subtotal (cuantos € se descuentan)
def calculate_discount(subtotal, discount_percent):
    discount = subtotal * discount_percent / Decimal("100") # discount_percent almacena el % de descuento que se aplica
    return discount


# Calcula los importes de una linea:
# El descuento global solo se aplica al calcular el IVA de la factura
def calculate_line(line):
    gross = line.quantity * line.unit_price
    return gross - calculate_discount(gross, line.discount_percent)


# Calcula los importes totales de una factura
def calculate_invoice_totals(lines, global_discount_percent):
    line_amounts = [(line, calculate_line(line)) for line in lines]

    subtotal = sum((amount for _, amount in line_amounts), Decimal("0"))
    discount_amount = calculate_discount(subtotal, global_discount_percent)

    # El descuento global se reparte proporcionalmente entre las líneas
    raw_bases = defaultdict(Decimal)
    for line, amount in line_amounts:
        taxable = amount - calculate_discount(amount, global_discount_percent)
        raw_bases[line.tax_rate] += taxable

    # Redondeo al final: base por tipo y, sobre esa base, la cuota
    base_breakdown = {rate: round_money(base) for rate, base in raw_bases.items()}
    tax_breakdown = {
        rate: round_money(base * rate / HUNDRED)
        for rate, base in base_breakdown.items()
    }

    taxable_base = sum(base_breakdown.values(), Decimal("0"))
    tax_amount = sum(tax_breakdown.values(), Decimal("0"))

    return {
        "subtotal": round_money(subtotal),
        "discount_amount": round_money(discount_amount),
        "taxable_base": taxable_base,
        "tax_amount": tax_amount,
        "base_breakdown": base_breakdown,
        "tax_breakdown": tax_breakdown,
        "total": taxable_base + tax_amount,
    }


# Calcular la cantidad total de artículos
def calculate_total_articles(lines):
    total_articles = sum(line.quantity for line in lines)

    return total_articles


# # Calcula los importes de una linea:
# # El descuento global solo se aplica al calcular el IVA de la factura
# def calculate_line(line, global_discount_percent):
#     gross = line.quantity * line.unit_price # Importe bruto
#     line_discount = calculate_discount(gross, line.discount_percent) # Euros de descuento de linea
#     line_amount = gross - line_discount # Cantidad * precio, aplicando descuento de esa linea
#     global_discount = calculate_discount(line_amount, global_discount_percent) #Euros de descuento global
#     taxable = line_amount - global_discount # Base para el IVA
#     tax_amount = taxable * line.tax_rate / Decimal("100") # IVA correspondiente a esa linea
#     return round_money(line_amount), round_money(tax_amount)


# # Calcula los importes totales de una factura
# def calculate_invoice_totals(lines, global_discount_percent):
#     subtotal = Decimal("0")
#     tax_amount = Decimal("0")

#     for line in lines:
#         line_amount, line_tax = calculate_line(line, global_discount_percent)
#         subtotal += line_amount
#         tax_amount += line_tax

#     discount_amount = round_money(calculate_discount(subtotal, global_discount_percent))
#     total = subtotal - discount_amount + tax_amount
    
#     return { # Importes redondeados
#         "subtotal": subtotal,
#         "discount_amount": discount_amount,
#         "tax_amount": tax_amount,
#         "total": total
#     }