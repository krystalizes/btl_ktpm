# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
# Create your models here.
class shipment(models.Model):
### The following are the fields of our table.
    id = models.AutoField(primary_key=True)
    orderid=models.IntegerField(default=0)
    status = models.CharField(max_length=20)
    mobile=models.CharField(max_length=255)
    shipping_address = models.CharField(max_length=200)
    shipping_method = models.CharField(max_length=200,default='')
    estimated_delivery_date=models.DateField()
    actual_delivery_date=models.DateField()
### It will help to print the values.
def __str__(self):
    return '%s %s %s %s %s %s %s %s' % (self.id, self.orderid, self.status, self.mobile, self.shipping_address, self.shipping_method, self.estimated_delivery_date , self.actual_delivery_date)