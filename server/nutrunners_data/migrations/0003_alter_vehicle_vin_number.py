# Generated by Django 4.0.6 on 2022-08-01 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrunners_data', '0002_remove_tightening_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='vin_number',
            field=models.CharField(max_length=18, unique=True),
        ),
    ]