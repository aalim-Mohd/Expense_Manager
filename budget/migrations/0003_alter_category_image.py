# Generated by Django 5.0.6 on 2024-08-16 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_category_image_alter_category_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(default='default.png', upload_to='c_images'),
        ),
    ]
