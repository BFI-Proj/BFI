# Generated by Django 4.2.5 on 2023-11-05 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_yourmodel_fooditem_image_alter_fooditem_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooditem',
            name='description',
            field=models.TextField(default='No Description'),
        ),
    ]
