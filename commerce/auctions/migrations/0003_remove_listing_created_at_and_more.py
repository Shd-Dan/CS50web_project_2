# Generated by Django 5.1.6 on 2025-06-04 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_listing_comment_bid_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='current_price',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='seller',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='winner',
        ),
    ]
