# Generated by Django 4.0.6 on 2022-08-02 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutrunners_data', '0004_rename_vin_number_tightening_vin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nutrunner',
            old_name='nutrunner_name',
            new_name='name',
        ),
    ]