from ninja import NinjaAPI
from apps.products.api import router as products_router
from apps.users.api import router as users_router
from apps.carts.api import router as carts_router
from apps.orders.api import router as orders_router

api = NinjaAPI(
    title="EC API",
    version="1.0.0",
    description="API for E-commerce Application"
)
api.add_router("/products", products_router)
api.add_router("/users", users_router)
api.add_router("/carts", carts_router)
api.add_router("/orders", orders_router)