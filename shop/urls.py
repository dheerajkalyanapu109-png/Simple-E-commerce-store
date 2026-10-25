from django.contrib.auth import views as auth
from django.urls import path
from . import views as v
urlpatterns = [
    path("", v.product_list, name="list"),
    path("product/<slug:slug>/", v.product_detail, name="detail"),
    path("cart/", v.cart_view, name="cart"),
    path("cart/add/<int:pid>/", v.cart_add, name="cart_add"),
    path("cart/update/<int:pid>/", v.cart_update, name="cart_update"),
    path("checkout/", v.checkout, name="checkout"),
    path("orders/", v.orders, name="orders"),
    path("register/", v.register, name="register"),
    path("login/", auth.LoginView.as_view(), name="login"),
    path("logout/", auth.LogoutView.as_view(), name="logout"),
]
