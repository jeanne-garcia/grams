# Generated by Django 2.1.4 on 2019-05-12 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0020_auto_20190307_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assets',
            name='balance',
            field=models.FloatField(default=0.0),
        ),
    ]
