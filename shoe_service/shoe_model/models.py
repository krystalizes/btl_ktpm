from django.db import models

# Create your models here.
class shoes(models.Model):
    ### The following are the fields of our table.
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    availability = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    price = models.IntegerField()

    ### It will help to print the values.
    def __str__(self):
        return '%s %s %s %s %s %s' % (self.id, self.name,
                                      self.brand, self.availability, self.description, self.price)
