# Generated by Django 5.0.4 on 2024-07-13 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_remove_order_created_at_remove_order_total_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='subscription',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]