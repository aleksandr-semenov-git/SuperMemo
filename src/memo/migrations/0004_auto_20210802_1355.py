# Generated by Django 3.1.2 on 2021-08-02 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memo', '0003_auto_20210730_0301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='done',
        ),
        migrations.RemoveField(
            model_name='question',
            name='goal',
        ),
        migrations.RemoveField(
            model_name='question',
            name='theme',
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='memo.goal')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, default=None, max_length=200)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='memo.section')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='lesson',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='memo.lesson', verbose_name='Цель'),
        ),
    ]
