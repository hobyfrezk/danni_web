# Generated by Django 3.1.3 on 2021-07-08 02:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0004_auto_20210708_0242'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='appointment',
            unique_together=set(),
        ),
    ]