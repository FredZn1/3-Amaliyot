from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return f"{self.name}"











