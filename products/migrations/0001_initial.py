# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Name of this product.', max_length=50)),
                ('price', models.FloatField(help_text=b'the price of this product.', verbose_name=b'price')),
                ('quantity', models.PositiveIntegerField(help_text=b'quantity in stock of this product.', verbose_name=b'quantity available')),
                ('image', models.ImageField(upload_to=products.models.get_img_path, verbose_name=b'product image')),
            ],
        ),
    ]
