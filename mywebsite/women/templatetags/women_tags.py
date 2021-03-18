from django import template
from women.models import *
from women.views import menu
"""
В этом файле хранятся все тэги проекта women, которые мы сами реализуем
"""


register = template.Library() # через создание экземпляра класса мы создаём новый пользовательский тэг

@register.simple_tag(name='getcats') # тут мы связываем функцию get_categories с тэгом register и получаем тэг декорированный фунцкцией
def get_categories(filter=None): # тут мы создаём функцию для нашего тэга register и устанавливаем по умолчанию один параметр
    if filter is None: # если параметр стоит по умолчанию, то просто выводи список объектов из модели Category
        return Category.objects.all()
    else: # если параметр передан в тэг
        return Category.objects.filter(pk=filter) # то отобразить из модели Category только объекты pk(primary key) со значением filter(а это наш принимаемый аргумент)

@register.inclusion_tag('women/list_categories.html') # вот сюда будет передаваться 'cats' и 'cat_selected'
def show_categories(sort=None, cat_selected=0): # функция отображения всех категорий
    if sort is None:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by( )
    return {'cats': cats, 'cat_selected': cat_selected} # параметр 'cats' будет автоматически передаваться в качестве аргумента декоторору

@register.inclusion_tag('women/main_menu.html')
def main_menu():
    return {'menu': menu}


'''
этот тэг реализует представляет собой ссылку на html страницу, в которую он передаёт словарь с аргментами из функции, которую декорирует,
а дальше этот "включающий тэг" вставляется в любой html документ с помощью {% %} и его содержимое включается сразу в этот html-документ
точн о также как мы передавали аргумент тут
def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с её id: {post_id}")

мы передаём нашему файлу html людой другой аргумент, который возвращает функция
а метод inclusion_tag добавляет этот словарь нашему файлу html
'''