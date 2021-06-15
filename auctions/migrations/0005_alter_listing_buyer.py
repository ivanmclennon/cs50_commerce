# Generated by Django 3.2.4 on 2021-06-14 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_listing_buyer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to=settings.AUTH_USER_MODEL),
        ),
    ]