import os

from django.db import models

def get_img_path(instance, filename):
    return os.path.join(instance.name, filename)

class Product(models.Model):
    MAX_LEN = 50
    name = models.CharField(max_length=MAX_LEN, help_text="Name of this product.")
    price = models.FloatField(verbose_name="price",  help_text="the price of this product.",)
    quantity = models.PositiveIntegerField(verbose_name="quantity available",
                                            help_text="quantity in stock of this product.",)
    image = models.ImageField(upload_to=get_img_path, verbose_name="product image", null=True, blank=True)
