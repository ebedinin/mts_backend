# Generated by Django 3.0.7 on 2021-02-10 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('certification_pc', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pc',
            name='act',
        ),
    ]
