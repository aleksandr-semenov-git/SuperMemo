# Generated by Django 3.2.5 on 2022-03-04 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memo', '0002_alter_goal_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]