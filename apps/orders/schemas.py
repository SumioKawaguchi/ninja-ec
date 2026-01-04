from ninja import Schema
from datetime import datetime
from apps.products.schemas import ProductOut

class OrderItemOut(Schema):
    id:int
    product: ProductOut
    quantity: int
    price: float
    
class OrderOut(Schema):
    id:int
    status:str
    total_amount: float
    items:list[OrderItemOut]
    created_at: datetime