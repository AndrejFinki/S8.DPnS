# Generated by Django 5.0.3 on 2025-05-15 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_image_is_processed"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="processed_image",
            field=models.ImageField(
                blank=True, null=True, upload_to="processed_images/"
            ),
        ),
    ]
