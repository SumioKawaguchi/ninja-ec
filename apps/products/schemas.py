from ninja import Schema
from decimal import Decimal

class CategoryIn(Schema):
    name:str
    
class CategoryOut(Schema):
    id:int
    name:str
    
class ProductIn(Schema):
    name:str
    description: str = ""
    price:Decimal
    stock:int = 0
    category_id: int
    is_active: bool = True
    
class ProductOut(Schema):
    id:int
    name:str
    description:str
    price:Decimal
    stock:int
    category: CategoryOut
    is_active:bool