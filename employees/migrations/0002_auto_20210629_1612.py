# Generated by Django 3.1.3 on 2021-06-29 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20210626_0614'),
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['created_at']},
        ),
        migrations.AddField(
            model_name='employee',
            name='services',
            field=models.ManyToManyField(to='products.Product'),
        ),
    ]
