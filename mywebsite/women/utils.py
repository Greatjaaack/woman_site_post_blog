from django.db.models import Count
from django.core.cache import cache # это нам нужно для того, чтобы отдельно какие-то данные помещать в кэш, а затем к ним обращаться ( это api низкого уровня )

from .models import *

'''
в этом файле мы добавляем все классы примеси
'''
menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная свзь", 'url_name': 'contact'},
        ]


class DataMixin:
    '''
    создаём примясь , так как есть повторяющиеся части в файле views.py
    '''
    paginate_by = 3 # кол-во элементов на одной странице ( пагинация )

    def get_user_context(self, **kwargs):
        context = kwargs

        # #КЭШИРОВАНИЕ
        # cats = cache.get('cats') # береём из кэша 'cats' данные и помещаем их в переменную cats
        # if not cats:
        #     cats = Category.objects.annotate(Count('women')) # сделать запрос из БД
        #     cats = cache.set('cats', cats, 60) # создаём кэш cats по имени 'cats', помещаем его в переменную cats и задаём срок в 60 сек

        cats = Category.objects.annotate(Count('women')) # чтобы выклчить кэширование - нужно закоментировать эту строчку и раскомментироваь блок кода выше

        user_menu = menu.copy() # делаем копию для того, чтобы не менять наш список
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['cats'] = cats
        context['menu'] = user_menu

        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        return context