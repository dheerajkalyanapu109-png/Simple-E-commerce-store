from django.conf import settings
from django.db import models
from django.urls import reverse

class Product(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=7, default="#7a9a7e", help_text="Card colour (hex)")
    created = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created"]
    def __str__(self): return self.name
    def get_absolute_url(self): return reverse("detail", args=[self.slug])

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    name = models.CharField(max_length=120)
    address = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="Placed")
    created = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created"]
    def __str__(self): return f"Order #{self.pk}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
    def line_total(self): return self.price * self.quantity
