# Generated by Django 4.0.6 on 2022-08-03 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrunners_data', '0005_rename_nutrunner_name_nutrunner_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tightening',
            name='time_of_creation',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
