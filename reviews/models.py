from django.db import models
from orders.models import Order

class Review(models.Model):
    class RatingChoices(models.IntegerChoices):
        ONE = 1, '1 Star'
        TWO = 2, '2 Stars'
        THREE = 3, '3 Stars'
        FOUR = 4, '4 Stars'
        FIVE = 5, '5 Stars'

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RatingChoices.choices)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.order.id} | {self.rating} Stars"
