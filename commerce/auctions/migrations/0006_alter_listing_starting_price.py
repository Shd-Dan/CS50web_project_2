# Generated by Django 5.1.4 on 2025-06-05 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_bid_id_alter_category_id_alter_comment_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='starting_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
