# Generated by Django 2.1.4 on 2019-03-16 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_auto_20190316_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='assets_transact',
            field=models.ManyToManyField(related_name='assets_transactions', to='assets.Assets'),
        ),
    ]