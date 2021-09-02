from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

from django.contrib import messages

from App_Order.models import Cart, Order
from App_Shop.models import Product


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(
        item=item, user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, "This item quantity have been updated!")
            return redirect("App_Shop:home")
        else:
            order.orderitems.add(order_item[0])
            messages.info(request, "This item was added to your cart.")
            return redirect("App_Shop:home")
    else:
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request, "This item have been added to your cart.")
        return redirect("App_Shop:home")


@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, "App_Order/cart.html", context={'carts': carts, "order": order})
    else:
        messages.warning(request, "You don't have any item in your cart")
        return redirect('App_Shop:home')


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)  #product theke anlam
    order_qs = Order.objects.filter(user=request.user, ordered=False) #order ache ki nai
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():  #order er cart gulote item ta ache ki na
            order_item = Cart.objects.filter(user=request.user,item=item,purchased=False)[0] #item er cart ta select kora. coz cart remove korbo.
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.info(request, "Your item has removed!")
            return redirect("App_Order:cart")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("App_Shop:home")
    else:
        messages.info(request, "You don't have any active order")
        return redirect("App_Shop:home")


@login_required
def increase_quantity(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(
                user=request.user, item=item, purchased=False)[0]
            order_item.quantity += 1
            order_item.save()
            messages.info(
                request, f"{item.name} quantity has been updated")
            return redirect("App_Order:cart")
        else:
            messages.info(
                request, f"{item.name} You don't have this item in your order")
            return redirect("App_Shop:home")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("App_Shop:home")


@login_required
def decrease_quantity(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(
                user=request.user, item=item, purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(
                    request, f"{item.name} quantity has been updated")
                return redirect("App_Order:cart")
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.info(
                    request, f"{item.name} item has removed from your cart!")
                return redirect("App_Order:cart")
        else:
            messages.info(
                request, f"{item.name} You don't have this item in your order")
            return redirect("App_Shop:home")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("App_Shop:home")
