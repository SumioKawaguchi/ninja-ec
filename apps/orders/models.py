from django.conf import settings
from django.db import models
from apps.products.models import Product

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', '保留中'
        CONFIRMED = 'CONFIRMED', '確定'
        SHIPPED = 'SHIPPED', '発送済み'
        DELIVERED = 'DELIVERED', '配達済み'
        CANCELED = 'CANCELED', 'キャンセル'
        
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order #${self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} X "