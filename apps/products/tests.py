import pytest
from ninja.testing import TestClient
from config.api import api
from apps.products.models import Product, Category
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture(scope="module")
def client():
    return TestClient(api)

@pytest.fixture
def category(db):
    return [
            Category.objects.create(name="電化製品"),
            Category.objects.create(name="本")
            ]

@pytest.fixture
def product(db, category):
    return Product.objects.create(
        name="イヤホン",
        price=4000,
        stock=100,
        category=category[0]
    )
    
@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        email="test@a.com",
        password="password123"
    )

@pytest.fixture
def auth_headers(user):
    token = jwt.encode(
        {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(days=1)
        },
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    return {"Authorization": f"Bearer {token}"}
    
def test_list_categories(client, category):
    response = client.get("/products/categories")
    assert response.status_code == 200
    assert len(response.json()) == 2
    
def test_list_products(client, product):
    response = client.get("/products/products")
    assert response.status_code == 200
    assert len(response.json()) == 1
    
# 正常系:存在するidの商品を取得
def test_get_product(client, product):
    response = client.get(f"/products/products/{product.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "イヤホン"
    assert data["price"] == "4000.00"

# 異常系:存在しないidの商品を取得
def test_get_product_not_found(db, client):
    response = client.get("/products/products/999")
    assert response.status_code == 404
    
# ======= 認証が必要なエンドポイントのテスト ========
# 正常系:商品を作成が成功する
def test_create_product(client, auth_headers, category):
    response = client.post(
        "/products/products",
        json={
            "name": "スマートホン",
            "price": 80000,
            "stock": 50,
            "category_id": category[0].id
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "スマートホン"

# 異常系:商品作成時の認証エラー
def test_create_product_unauthorized(client, category):
    response = client.post(
        "/products/products",
        json={
            "name": "スマートホン",
            "price": 80000,
            "stock": 50,
            "category_id": category[0].id
        }
    )
    assert response.status_code == 401
    
# 異常系:商品作成時のパラメーターが不正
def test_create_product_invalid_params(client, auth_headers):
    response = client.post(
        "/products/products",
        json={
            "name": "スマートホン",
            "price": 20000,
            "stock": 10,
        },
        headers=auth_headers
    )
    assert response.status_code == 422
    
# 正常系:商品更新が成功する
def test_update_product(client, auth_headers, product, category):
    response = client.put(
        f"/products/products/{product.id}",
        json={
            "name": "高級イヤホン",
            "price": 50000,
            "stock": 80,
            "category_id": category[0].id
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "高級イヤホン"
    
# 異常系:商品更新時の認証エラー
def test_update_product_unauthorized(client, product, category):
    response = client.put(
        f"/products/products/{product.id}",
        json={
            "name": "高級イヤホン",
            "price": 50000,
            "stock": 80,
            "category_id": category[0].id
        }
    )
    assert response.status_code == 401
    
# 異常系:商品更新時のパラメーターが不正
def test_update_product_invalid_params(client, auth_headers, product):
    response = client.put(
        f"/products/products/{product.id}",
        json={
            "name": "廉価版イヤホン",
            "price": 4000,
            "stock": 100,
        },
        headers=auth_headers
    )
    assert response.status_code == 422
    
# 異常系:存在しないidの商品を更新
def test_update_product_not_found(client, auth_headers, category):
    response = client.put(
        "/products/products/999",
        json={
            "name": "高級イヤホン",
            "price": 50000,
            "stock": 80,
            "category_id": category[0].id
        },
        headers=auth_headers
    )
    assert response.status_code == 404
            