from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator
from django.db import models
from decimal import Decimal
from django.utils.crypto import get_random_string

from main.models import Destination

User = get_user_model()


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, destination_id, quantity, price):
        destination_id = str(destination_id)
        if destination_id not in self.cart:
            self.cart[destination_id] = {
                'quantity': quantity,
                'price': price
            }
            self.save()

    def remove(self, destination_id):
        destination_id = str(destination_id)
        if destination_id in self.cart:
            del self.cart[destination_id]
            self.save()

    def clean(self):
        for destination_id in self.cart:
            self.remove(destination_id)

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def __iter__(self):
        destinations_ids = self.cart.keys()
        destinations = Destination.objects.filter(id__in=destinations_ids)
        for destination in destinations:
            self.cart[str(destination.id)]['destination'] = destination

        for tour in self.cart.values():
            tour['total_price'] = Decimal(tour['price']) * tour['quantity']
            yield tour

    def __len__(self):
        return len(self.cart)

    def get_total_price(self):
        return sum(Decimal(item['price'] * item['quantity'])
                    for item in self.cart.values())

    def increment_quantity(self, destination_id):
        destination_id = str(destination_id)
        if destination_id in self.cart:
            if self.cart[destination_id]['quantity'] < 20:
                self.cart[destination_id]['quantity'] += 1
                self.save()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=6, blank=True, null=True)

    def create_activation_code(self):
        code = get_random_string(6)
        self.activation_code = code
        self.save()

    def send_activation_mail(self):
        self.create_activation_code()
        message = f'http://localhost:8000/order/activate{self.activation_code}/'
        send_mail(
            'Confirmation order',
            message,
            'test@gmail.com',
            [self.user.email]
        )

    def send_mail(self):
        if self.is_active:
            message = 'Your order been accepted'
            send_mail(
                'Order',
                message,
                'test@gmail.com',
                [self.user.email]
            )
        else:
            message = "Your order has not been confirmed. Please,confirm"
            send_mail(
                'Order',
                message,
                'test@gmail.com',
                [self.user.email]
            )


class OrderTour(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tours')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField(validators=[MaxValueValidator(4)])


