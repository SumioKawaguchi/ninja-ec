from ninja import Router
from django.shortcuts import get_object_or_404
from apps.users.auth import JWTAuth
from apps.products.models import Product
from .models import Cart, CartItem
from .schemas import CartItemIn,CartOut

router = Router(auth=JWTAuth(), tags=["Carts"])

@router.get("/", response=CartOut)
def get_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.auth)
    return cart

@router.post("/items", response=CartOut)
def add_item(request, payload: CartItemIn):
    cart, _ = Cart.objects.get_or_create(user=request.auth)
    product = get_object_or_404(Product, id=payload.product_id)
    
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': payload.quantity}
    )
    if not created:
        item.quantity += payload.quantity
        item.save()
    
    return cart

@router.put("/items/{product_id}", response=CartOut)
def update_item(request, product_id: int, payload: CartItemIn):
    cart = get_object_or_404(Cart, user=request.auth)
    item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    item.quantity = payload.quantity
    item.save()
    return cart

@router.delete("/items/{product_id}", response=CartOut)
def remove_item(request, product_id: int):
    cart = get_object_or_404(Cart, user=request.auth)
    item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    item.delete()
    return cart

@router.delete("/", response=dict)
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.auth)
    cart.items.all().delete()
    return {"detail": "Cart cleared"}