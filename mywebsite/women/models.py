from django.db import models
from django.urls import reverse


class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL') # тут мы создаём специальное название, которое будет добавлено в url, при переходе по этой ссылке для отображения в адресной строке
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фотография')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT,verbose_name='Профессия')

    def __str__(self):
        return self.title

    def get_absolute_url(self): # определяем функцию для добавления к названию адреса slug поста
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        '''
        отображения таблицы в админке
        '''
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['-time_create', 'time_update']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self): # определяем функцию для добавления к названию адреса slug поста
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        '''
        тут мы именуем отображения таблицы в админке
        '''
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']