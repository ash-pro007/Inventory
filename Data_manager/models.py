from django.db import models

# Create your models here.

class Inventory(models.Model):
    name = models.CharField(max_length=12, primary_key=True)


class Product(models.Model):
    name = models.CharField(max_length=10, primary_key=True)


class Products_in_inventories(models.Model):
    name = models.CharField(max_length=25, primary_key=True)