# Generated by Django 3.0.4 on 2020-03-09 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20200309_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
