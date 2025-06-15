from django.db import migrations, models
import django.db.models.deletion

def populate_categories(apps, schema_editor):
    Category = apps.get_model('auctions', 'Category')
    categories = [
        "Fashion", "Toys", "Electronics", "Home", "Books", "Sports",
        "Jewelry", "Art", "Collectibles", "Automotive", "Garden",
        "Music", "Movies", "Gaming", "Health", "Beauty", "Other"
    ]
    for category in categories:
        Category.objects.create(name=category)

class Migration(migrations.Migration):
    dependencies = [
        ('auctions', '0006_alter_listing_starting_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='starting_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='auctions.user'),
        ),
        migrations.RunPython(populate_categories),
    ] 