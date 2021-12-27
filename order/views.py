from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View

from main.models import Destination
from order.forms import AddToCartForm
from order.models import Cart, Order, OrderTour


class AddToCartView(View):
    def post(self, request, destination_id):
        cart = Cart(request)
        destination = get_object_or_404(Destination, id=destination_id)
        form = AddToCartForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            quantity = data.get('quantity')
            cart.add(destination.id, quantity, str(destination.price))
        return redirect(reverse_lazy('cart-details'))


class RemoveFromCartView(View):
    def get(self, request, destination_id):
        cart = Cart(request)
        destination = get_object_or_404(Destination, id=destination_id)
        cart.remove(destination.id)
        return redirect(reverse_lazy('cart-details'))


class CartDetailsView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'order/cart_details.html', {'cart': cart})


class IncrementQuantityView(View):
    def get(self, request, destination_id):
        cart = Cart(request)
        destination = get_object_or_404(Destination, id=destination_id)
        cart.increment_quantity(destination.id)
        return redirect(reverse_lazy('cart-details'))


class CreateOrderView(View):
    def get(self, request):
        session_cart = Cart(request)
        if not session_cart.cart:
            return redirect(reverse_lazy('index'))
        order = Order(user=request.user, total_price=session_cart.get_total_price())
        for tour, values in session_cart.cart.tours():
            destination = Destination.objects.get(id=id)
            OrderTour(order=order, destination=destination, quantity=values.get("quantity"))
            session_cart.clean()
            order.send_activation_mail()


class ActivationOrderView(View):
    def get(self, request, activation_code):
        order = Order.objects.get(user=request.user, activation_code=activation_code)
        order.is_active = True
        order.save()
        order.send_mail()


