# Generated by Django 5.1.7 on 2025-03-08 07:22

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Order",
            new_name="Orders",
        ),
        migrations.RenameField(
            model_name="products",
            old_name="proce",
            new_name="price",
        ),
    ]
