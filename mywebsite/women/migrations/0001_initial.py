# Generated by Django 3.1.7 on 2021-03-07 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Категория')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категорити',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Women',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('content', models.TextField(blank=True, verbose_name='Текст статьи')),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фотография')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('is_published', models.BooleanField(default=True, verbose_name='Статус публикации')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='women.category', verbose_name='Профессия')),
            ],
            options={
                'verbose_name': 'Известные женщины',
                'verbose_name_plural': 'Известные женщины',
                'ordering': ['time_create', 'time_update'],
            },
        ),
    ]
