from __future__ import unicode_literals
from django.db import models
# This is our model for user registration.
class books(models.Model):
    ### The following are the fields of our table.
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    availability = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    price = models.IntegerField()

    ### It will help to print the values.
    def __str__(self):
        return '%s %s %s %s %s %s' % (self.id, self.name,
                                      self.author, self.availability, self.description, self.price)
