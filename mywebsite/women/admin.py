from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class WomenAdmin(admin.ModelAdmin):
    '''
    поля в админке
    '''
    list_display = ['id', 'title', 'time_create', 'get_html_photo', 'is_published'] # прописываем здесь функцию get_html_photo, которая возвращает html-код, который подставляется в html и отображает миниатюру изображения
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title", )}
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update') #этот атрибут содержит порядок и список редактируемых полей, которые нужно отображать в форме редактирования
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')#этот атриут нужен для того, чтобы объявить поля только для чтения , а затем выше мы их уже можем отобразить
    save_on_top = True

    def get_html_photo(self, object):
        '''
        прописываем эту функцию для того, чтобы вместо адреса пути фотографий, отображалась миниатюра этой фотографи
        '''
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=80") # mark_safe - эту функция позволяет не эканировать тэг, и выполнять их

    get_html_photo.short_description = 'Мини-фотография' # так мы меняем название колонки фоторафии, так как именно данная функция выступает в качестве поля

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    list_display_links = ('name', 'id')
    search_fields = ('name', )
    prepopulated_fields = {"slug": ("name", )} # пишет транслитом поле name и заполняет поле slug

admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админ-панель сайта о женщинах'
admin.site.site_header =  'Админ-панель сайта о женщинах'
