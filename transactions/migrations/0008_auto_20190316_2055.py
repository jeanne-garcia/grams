# Generated by Django 2.1.4 on 2019-03-16 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_auto_20190316_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]