# Generated by Django 4.0 on 2022-11-09 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0057_payment_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='order',
        ),
    ]