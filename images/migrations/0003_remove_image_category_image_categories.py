# Generated by Django 5.0.4 on 2024-06-20 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_category_remove_image_uploaded_at_alter_image_title_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='category',
        ),
        migrations.AddField(
            model_name='image',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='images', to='images.category'),
        ),
    ]
