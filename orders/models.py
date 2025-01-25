from django.db import models
from django.contrib.auth import get_user_model

from shop.models import Product

class Order(models.Model):
    """ Represents an order made by a user. """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="orders")
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(blank=True, null=True, default=None)

    class Meta:
        ordering = ("paid", "-updated")

    def __str__(self):
        return f"{self.user} - {str(self.id)}"

class OrderItem(models.Model):
    """ Represents an item within an order.
    Links a product to an order with quantity and price."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity