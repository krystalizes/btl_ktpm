from __future__ import unicode_literals
from django.db import models
# This is our model for user registration.
class carts(models.Model):
    customerid = models.IntegerField(default=0)
    product_id = models.CharField(max_length=10)
    quantity = models.CharField(max_length=5)
    price=models.IntegerField(default=0)
### It will help to print the values.
def __str__(self):
    return '%s %s %s %s %s' % (self.customerid, self.product_id, self.quantity, self.price)