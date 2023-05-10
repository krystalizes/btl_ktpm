from django.db import models

# Create your models here.
class user(models.Model):
    id = models.AutoField(primary_key=True)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    role=models.IntegerField(default=0)
    def __str__(self):
        return '%s %s %s %s' % (self.id, self.email, self.password,self.role)
class customer(models.Model):
    id = models.AutoField(primary_key=True)
    uid=models.ForeignKey(user,on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    def __str__(self):
        return '%s %s %s %s %s' % (self.id, self.uid, self.name,self.phone,self.address)