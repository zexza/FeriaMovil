from django import template
register = template.Library()


@register.filter()
def multiply(precio, cantidad):
    preciofinal =float(precio) * cantidad
    # FprecioM=(f'{preciofinal:.3f}')
    FprecioM = int(preciofinal)
    return FprecioM


@register.filter()
def money_format(value, arg):
    return f"{value}{arg}"

@register.filter()
def descuento(precio, desc):
    descuento =(desc/100)*precio
    preciofinal =float(precio-descuento)
    FprecioD= int(preciofinal)
    return FprecioD
# prefiofinal en float manejar despues con formato decimal de la misma manera en otro metodo
