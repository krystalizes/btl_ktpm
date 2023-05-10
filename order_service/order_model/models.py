from django.db import models

# Create your models here.
class order(models.Model):
    id = models.AutoField(primary_key=True)
    customerid=models.IntegerField(default=0)
    productlist=models.CharField(max_length=255)
    quantity=models.IntegerField(default=0)
    price=models.IntegerField(default=0)
    status=models.CharField(max_length=255)
    created_at=models.DateTimeField()

    def __str__(self):
        return '%s %s %s %s %s %s %s' % (self.id, self.customerid, self.productlist,self.quantity,self.price,self.status,self.created_at)