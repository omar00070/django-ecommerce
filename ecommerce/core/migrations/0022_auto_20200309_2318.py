# Generated by Django 3.0.4 on 2020-03-09 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_banners'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banners',
            old_name='first_image',
            new_name='banner_image',
        ),
        migrations.RemoveField(
            model_name='banners',
            name='second_image',
        ),
        migrations.RemoveField(
            model_name='banners',
            name='third_image',
        ),
    ]
