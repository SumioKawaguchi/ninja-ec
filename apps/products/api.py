from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Product, Category
from .schemas import ProductIn, ProductOut, CategoryOut, CategoryIn
from apps.users.auth import JWTAuth

router = Router()

# ======== Category Endpoints ========
@router.get("/categories", response=list[CategoryOut])
def get_categories(request):
    categories = Category.objects.all()
    return categories

@router.post("/categories", response=CategoryOut, auth=JWTAuth())
def create_category(request, payload:CategoryIn):
    category = Category.objects.create(**payload.dict())
    return category

# ======== Product Endpoints ========
@router.get("/products", response=list[ProductOut])
def get_products(request):
    products = Product.objects.select_related('category').filter(is_active=True)
    return products

@router.get("/products/{product_id}", response=ProductOut)
def get_product(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    return product

@router.post("/products", response=ProductOut, auth=JWTAuth())
def create_product(request, payload:ProductIn):
    product = Product.objects.create(**payload.dict())
    return product

@router.put("/products/{product_id}", response=ProductOut, auth=JWTAuth())
def update_product(request, product_id:int, payload:ProductIn):
    product = get_object_or_404(Product, id=product_id)
    for attr, value in payload.dict().items():
        setattr(product, attr, value)
    product.save()
    return product
    
@router.delete("/products/{product_id}", auth=JWTAuth())
def delete_product(request, product_id:int):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return {"success": True}