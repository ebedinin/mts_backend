# Generated by Django 3.0.7 on 2021-02-10 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('certification_pc', '0002_remove_pc_act'),
    ]

    operations = [
        migrations.AddField(
            model_name='pc',
            name='act',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='certification_pc.Act'),
        ),
    ]
