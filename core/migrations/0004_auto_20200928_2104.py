# Generated by Django 3.1.1 on 2020-09-28 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200928_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, upload_to='items/'),
        ),
    ]
