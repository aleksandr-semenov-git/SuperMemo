# Generated by Django 3.1.2 on 2022-02-03 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repeat', '0004_auto_20220128_1344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repetitionsession',
            name='is_ended',
        ),
        migrations.RemoveField(
            model_name='repetitionsession',
            name='is_paused',
        ),
        migrations.RemoveField(
            model_name='repetitionsession',
            name='is_started',
        ),
        migrations.AddField(
            model_name='repetitionsession',
            name='status',
            field=models.CharField(choices=[('IP', 'in progress'), ('F', 'fin'), ('P', 'paused')], default='IP', max_length=11),
        ),
        migrations.AlterField(
            model_name='repetitionsession',
            name='rep_mod',
            field=models.CharField(choices=[('M', 'Mix'), ('G', 'Goal'), ('S', 'Section'), ('T', 'Theme')], default='M', max_length=7),
        ),
    ]
