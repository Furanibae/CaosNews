# Generated by Django 5.0.4 on 2024-07-14 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_remove_subscription_price_subscription_price_usd'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='price_usd',
        ),
        migrations.AddField(
            model_name='subscription',
            name='price',
            field=models.IntegerField(default=1),
        ),
    ]