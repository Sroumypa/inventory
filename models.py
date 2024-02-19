from django.db import models
from django.contrib.auth.models import User

class Inventory(models.Model):
    product_id = models.CharField(max_length=256, unique=True)
    product_name = models.CharField(max_length=256)
    vendor = models.CharField(max_length=100)
    mrp = models.FloatField()
    batch_num = models.CharField(max_length=256)
    batch_date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    status = models.CharField(max_length=256)

class Userp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roles = models.ManyToManyField("Role")
class Role(models.Model):
    name = models.CharField(max_length=256, unique=True)



