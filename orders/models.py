from django.db import models

from shop.models import Product

# Create your models here.

class Order(models.Model):
    """
    The Order model contains several fields to store customer information.
    A model to store the order details.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)   
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"])
        ]
    def __str__(self):
        return f"Order {self.id}"
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
class OrderItem(models.Model):
    """
    Represents an item within an order in the online store.
    Model to store items bought, including their price and quantity.
    Attributes:
        order (Order): The order to which this item belongs.
        product (Product): The product associated with this item.
        price (Decimal): The price of the product.
        quantity (PositiveIntegerField): The quantity of the product in this order item.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        """
        Calculates the total cost of this order item.

        Returns:
            Decimal: The total cost of this order item (price * quantity).
        """
        return self.price * self.quantity