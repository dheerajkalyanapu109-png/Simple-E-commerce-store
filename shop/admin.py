from django.contrib import admin
from .models import Product, Order, OrderItem
class ItemInline(admin.TabularInline):
    model = OrderItem; extra = 0
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock"); prepopulated_fields = {"slug": ("name",)}
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total", "status", "created"); list_editable = ("status",); inlines = [ItemInline]
