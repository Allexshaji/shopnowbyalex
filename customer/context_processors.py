from .models import Cart, CartItem

def cart_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            count = CartItem.objects.filter(cart=cart).count()
        else:
            count = 0
    else:
        count = 0
    return {
        'cart_count': count
    }
