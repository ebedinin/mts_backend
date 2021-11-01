# Generated by Django 3.0.7 on 2021-02-10 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_abbreviation', models.CharField(max_length=50)),
                ('name_full', models.CharField(blank=True, default='', max_length=500)),
                ('isActive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('serial_number', models.CharField(blank=True, max_length=500, null=True)),
                ('inventory_number', models.CharField(blank=True, max_length=50, null=True)),
                ('date_input', models.DateTimeField(blank=True, null=True)),
                ('price_start_up', models.DecimalField(blank=True, decimal_places=2, default=True, max_digits=10, null=True)),
                ('date_debit', models.DateTimeField(blank=True, null=True)),
                ('provisioner', models.CharField(blank=True, max_length=500, null=True)),
                ('decree', models.CharField(blank=True, max_length=500, null=True)),
                ('delivery_plan', models.CharField(blank=True, max_length=100, null=True)),
                ('invoice', models.CharField(blank=True, max_length=100, null=True)),
                ('date_start', models.DateField(blank=True, max_length=100, null=True)),
                ('date_stop', models.DateTimeField(blank=True, max_length=100, null=True)),
                ('note', models.TextField(default='1', verbose_name='Описание')),
                ('isActive', models.BooleanField(default=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mts.Department')),
                ('device_prev', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mts.Device')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('isActive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceProfileField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('isActive', models.BooleanField(default=True)),
                ('device_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='mts.DeviceProfile')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('isActive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ovd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_abbreviation', models.CharField(max_length=200)),
                ('name_full', models.CharField(blank=True, default='', max_length=200)),
                ('isActive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('type', models.CharField(choices=[('REPORT_DEVICE_PROFILE', 'Отчёт по профилям устройств'), ('REPORT_DEVICE_AVAILABLE', 'Отчёт о наличии устройств')], max_length=50)),
                ('isActive', models.BooleanField(default=True)),
                ('device_profile', models.ManyToManyField(blank=True, to='mts.DeviceProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Timesheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('note', models.TextField()),
                ('isActive', models.BooleanField(default=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mts.Department')),
            ],
        ),
        migrations.CreateModel(
            name='ReportDeviceProfileDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=500, null=True)),
                ('isActive', models.BooleanField(default=True)),
                ('device_profile_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mts.DeviceProfileField')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mts.Report')),
            ],
        ),
        migrations.CreateModel(
            name='Nomenclature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_1', models.IntegerField(blank=True, verbose_name='Номер 1')),
                ('number_2', models.IntegerField(blank=True, verbose_name='Номер 2')),
                ('number_3', models.IntegerField(blank=True, verbose_name='Номер 3')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('note', models.TextField(verbose_name='Описание')),
                ('isActive', models.BooleanField(default=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mts.Department', verbose_name='Подразделение')),
            ],
        ),
        migrations.CreateModel(
            name='NecessaryQuantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('isActive', models.BooleanField(default=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mts.Department')),
                ('nomenclature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mts.Nomenclature')),
                ('ovd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mts.Ovd')),
                ('timesheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mts.Timesheet')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=500)),
                ('isActive', models.BooleanField(default=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mts.Device')),
                ('device_profile_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mts.DeviceProfileField')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='device_profile',
            field=models.ManyToManyField(blank=True, to='mts.DeviceProfile'),
        ),
        migrations.AddField(
            model_name='device',
            name='nomenclature',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mts.Nomenclature'),
        ),
        migrations.AddField(
            model_name='device',
            name='ovd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mts.Ovd'),
        ),
        migrations.AddField(
            model_name='device',
            name='status',
            field=models.ManyToManyField(to='mts.DeviceStatus'),
        ),
        migrations.AddField(
            model_name='department',
            name='ovd',
            field=models.ManyToManyField(to='mts.Ovd', verbose_name='ОВД'),
        ),
    ]