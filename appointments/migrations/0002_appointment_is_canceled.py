# Generated by Django 3.1.3 on 2021-07-07 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='is_canceled',
            field=models.BooleanField(default=False),
        ),
    ]