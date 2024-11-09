# Generated by Django 5.0.6 on 2024-08-13 13:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='c_images'),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('name', 'owner')},
        ),
    ]
