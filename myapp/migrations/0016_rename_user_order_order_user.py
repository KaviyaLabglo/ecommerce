# Generated by Django 4.0 on 2022-10-22 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='user',
            new_name='order_user',
        ),
    ]