from django.db import models

# Create your models here.
class payment(models.Model):
    id = models.AutoField(primary_key=True)
    orderid=models.IntegerField(default=0)
    status = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=200)
    price=models.IntegerField(default=0)
    payment_done_date=models.DateTimeField()

    def __str__(self):
        return '%s %s %s %s %s %s' % (self.id, self.orderid, self.status,self.payment_method,self.price,self.payment_done_date)