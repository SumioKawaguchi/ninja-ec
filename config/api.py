from ninja import NinjaAPI
from apps.products.api import router as products_router
from apps.users.api import router as users_router
from apps.carts.api import router as carts_router

api = NinjaAPI()
api.add_router("/products", products_router)
api.add_router("/users", users_router)
api.add_router("/carts", carts_router)