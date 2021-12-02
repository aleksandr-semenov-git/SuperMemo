# Generated by Django 3.1.2 on 2021-11-24 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField(default=1)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('end', models.DateTimeField(auto_now=True)),
                ('goal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='memo.goal', verbose_name='goal')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('goal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='memo.goal', verbose_name='goal')),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, null=True)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='themes', to='memo.section', verbose_name='section')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500, null=True)),
                ('answer', models.CharField(max_length=500, null=True)),
                ('lesson', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='memo.lesson', verbose_name='lesson')),
                ('theme', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='memo.theme', verbose_name='theme')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(default='user_images/default.jpg', upload_to='user_images/%Y/%m/%d')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='memo.profile', verbose_name='profile'),
        ),
        migrations.AddField(
            model_name='goal',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='goals', to='memo.profile', verbose_name='profile'),
        ),
    ]
