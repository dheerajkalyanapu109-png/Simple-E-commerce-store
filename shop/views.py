from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Product, Order, OrderItem

def product_list(request):
    q = request.GET.get("q", "").strip()
    products = Product.objects.filter(name__icontains=q) if q else Product.objects.all()
    return render(request, "list.html", {"products": products, "q": q})

def product_detail(request, slug):
    return render(request, "detail.html", {"product": get_object_or_404(Product, slug=slug)})

def _cart(request):
    cart = request.session.get("cart", {})
    items, total = [], Decimal("0")
    for p in Product.objects.filter(id__in=[int(k) for k in cart]):
        qty = cart[str(p.id)]
        items.append({"product": p, "qty": qty, "line": p.price * qty}); total += p.price * qty
    return items, total

def cart_view(request):
    items, total = _cart(request)
    return render(request, "cart.html", {"items": items, "total": total})

@require_POST
def cart_add(request, pid):
    p = get_object_or_404(Product, pk=pid)
    cart = request.session.get("cart", {})
    qty = min(cart.get(str(pid), 0) + max(int(request.POST.get("qty", 1) or 1), 1), p.stock)
    if qty > 0: cart[str(pid)] = qty
    request.session["cart"] = cart
    if request.headers.get("x-requested-with") == "fetch":
        return JsonResponse({"count": sum(cart.values()), "name": p.name})
    return redirect("cart")

@require_POST
def cart_update(request, pid):
    cart = request.session.get("cart", {})
    p = get_object_or_404(Product, pk=pid)
    qty = min(max(int(request.POST.get("qty", 0) or 0), 0), p.stock)
    if qty: cart[str(pid)] = qty
    else: cart.pop(str(pid), None)
    request.session["cart"] = cart
    return redirect("cart")

@login_required
def checkout(request):
    items, total = _cart(request)
    if not items:
        return redirect("cart")
    if request.method == "POST":
        name, address = request.POST.get("name", "").strip(), request.POST.get("address", "").strip()
        if not (name and address):
            messages.error(request, "Enter your name and delivery address.")
        else:
            try:
                with transaction.atomic():
                    order = Order.objects.create(user=request.user, name=name, address=address, total=total)
                    for it in items:
                        p = Product.objects.select_for_update().get(pk=it["product"].pk)
                        if p.stock < it["qty"]:
                            raise ValueError(f"Only {p.stock} of {p.name} left.")
                        p.stock -= it["qty"]; p.save()
                        OrderItem.objects.create(order=order, product=p, price=p.price, quantity=it["qty"])
            except ValueError as e:
                messages.error(request, str(e)); return redirect("cart")
            request.session["cart"] = {}
            messages.success(request, f"Order #{order.pk} placed. Thank you!")
            return redirect("orders")
    return render(request, "checkout.html", {"items": items, "total": total})

@login_required
def orders(request):
    return render(request, "orders.html", {"orders": request.user.orders.prefetch_related("items__product")})

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save()); return redirect("list")
    return render(request, "registration/register.html", {"form": form})
