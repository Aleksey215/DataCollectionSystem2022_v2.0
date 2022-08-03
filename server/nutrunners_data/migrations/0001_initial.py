# Generated by Django 4.0.6 on 2022-07-31 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nutrunner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nutrunner_name', models.CharField(max_length=16, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductionLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vin_number', models.CharField(max_length=16, unique=True)),
                ('model', models.CharField(max_length=8, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tightening',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=16)),
                ('time_of_creation', models.DateTimeField()),
                ('printing', models.BooleanField(blank=True, default=False, null=True)),
                ('torque_1', models.FloatField(blank=True, null=True)),
                ('torque_2', models.FloatField(blank=True, null=True)),
                ('torque_3', models.FloatField(blank=True, null=True)),
                ('torque_4', models.FloatField(blank=True, null=True)),
                ('torque_5', models.FloatField(blank=True, null=True)),
                ('torque_6', models.FloatField(blank=True, null=True)),
                ('torque_7', models.FloatField(blank=True, null=True)),
                ('torque_8', models.FloatField(blank=True, null=True)),
                ('torque_9', models.FloatField(blank=True, null=True)),
                ('torque_10', models.FloatField(blank=True, null=True)),
                ('status_1', models.CharField(blank=True, max_length=4, null=True)),
                ('status_2', models.CharField(blank=True, max_length=4, null=True)),
                ('status_3', models.CharField(blank=True, max_length=4, null=True)),
                ('status_4', models.CharField(blank=True, max_length=4, null=True)),
                ('status_5', models.CharField(blank=True, max_length=4, null=True)),
                ('status_6', models.CharField(blank=True, max_length=4, null=True)),
                ('status_7', models.CharField(blank=True, max_length=4, null=True)),
                ('status_8', models.CharField(blank=True, max_length=4, null=True)),
                ('status_9', models.CharField(blank=True, max_length=4, null=True)),
                ('status_10', models.CharField(blank=True, max_length=4, null=True)),
                ('nutrunner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nutrunners_data.nutrunner')),
                ('vin_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nutrunners_data.vehicle')),
            ],
        ),
        migrations.AddField(
            model_name='nutrunner',
            name='production_line',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nutrunners_data.productionline'),
        ),
    ]