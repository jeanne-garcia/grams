# Generated by Django 2.1.4 on 2019-02-28 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0009_auto_20190223_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assets',
            name='status',
            field=models.CharField(choices=[('In Use', 'In Use'), ('In Storage', 'In Storage'), ('In Maintenance', 'In Maintenance'), ('Defective', 'Defective'), ('Archived', 'Archived')], max_length=100),
        ),
    ]
