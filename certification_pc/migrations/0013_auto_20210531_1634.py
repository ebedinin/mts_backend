# Generated by Django 3.0.7 on 2021-05-31 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification_pc', '0012_auto_20210531_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logpcedit',
            name='vipnet_identifier',
            field=models.CharField(blank=True, default='', max_length=10, null=True),
        ),
    ]
