# Generated by Django 2.1.4 on 2019-03-06 18:21

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0018_auto_20190306_2252'),
    ]

    operations = [
        migrations.AddField(
            model_name='assets',
            name='depreciate',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='assets',
            name='it_accrued',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), null=True, size=None),
        ),
        migrations.AddField(
            model_name='assets',
            name='it_balance',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), null=True, size=None),
        ),
        migrations.AddField(
            model_name='assets',
            name='it_dep_date',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DateField(), null=True, size=None),
        ),
    ]
