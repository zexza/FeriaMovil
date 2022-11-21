def cart_total_amount(request):
    total = 0
    FprecioC = 0
    if request.user.is_authenticated:
        for key, value in request.session['cart'].items():
            total = total + (float(value['price']) * value['quantity'])
            # FprecioC=(f'{total:.3f}')
            FprecioC= int(total)
    return {'cart_total_amount': FprecioC}
