from ninja import Schema
from apps.products.schemas import ProductOut

class CartItemIn(Schema):
    product_id: int
    quantity: int = 1
    
class CartItemOut(Schema):
    id: int
    product: ProductOut
    quantity: int
    
class CartOut(Schema):
    id: int
    items: list[CartItemOut]