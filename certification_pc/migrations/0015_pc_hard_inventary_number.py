# Generated by Django 3.0.7 on 2021-06-01 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification_pc', '0014_pc_date_exclude'),
    ]

    operations = [
        migrations.AddField(
            model_name='pc',
            name='hard_inventary_number',
            field=models.CharField(blank=True, default=None, max_length=500, null=True),
        ),
    ]