from django.shortcuts import get_object_or_404
from apps.carts.models import Cart
from apps.orders.models import Order, OrderItem
from apps.orders.schemas import OrderItemOut, OrderOut
from apps.users.auth import JWTAuth
from ninja import Router

router = Router(tags=["Orders"], auth=JWTAuth())

@router.post("/", response=OrderOut)
def create_order(request):
    cart = get_object_or_404(Cart, user=request.auth)
    
    if not cart.items.exists():
        return {"error" : "Cart is empty."}
    
    total = sum(item.product.price * item.quantity for item in cart.items.all())
    
    order = Order.objects.create(
        user=request.auth,
        total_amount=total
    )
    
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
    cart.items.all().delete()
    
    return order

@router.get("/", response=list[OrderOut])
def list_orders(request):
    return Order.objects.filter(user=request.auth).order_by('-created_at')

@router.get("/{order_id}", response=OrderOut)
def get_order(request, order_id: int):
    order = get_object_or_404(Order, id=order_id, user=request.auth)
    return order