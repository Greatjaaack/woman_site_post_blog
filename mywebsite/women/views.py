from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *


# menu = [{'title': "О сайте", 'url_name': 'about'},
#         {'title': "Добавить статью", 'url_name': 'add_page'},
#         {'title': "Обратная свзь", 'url_name': 'contact'},
#         {'title': "Войти", 'url_name': 'login'}
#         ]


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        '''
        добавим фильтрацию статей по флагу is_published, будем отображать только опубликованные статьи
        '''
        return Women.objects.filter(is_published=True).select_related('cat')


class AboutThisWebSite(DataMixin,ListView):
    model = Women
    template_name = 'women/about.html'
    context_object_name = 'about'

    def get_context_data(self, **kwargs):
        #context = super().get_context_data()
        c_def = self.get_user_context(title='О сайте')
        return c_def #dict(list(context.items()) + list(c_def.items()))

#def about_us(request):
#    return render(request, 'women/about.html', {'menu': menu, 'title': 'О чём сайт'})

class ContactFromView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(**kwargs)
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None ,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class AddPage(LoginRequiredMixin ,DataMixin, CreateView):
    form_class = AddPostForim
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home') # если добавление статьи прошло успешно, то лениво перекидывает на страницу 'home'
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None ,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))


class WomenCategory(DataMixin, ListView):
    '''
    определяем класс для отображения категорий по фильтрам
    '''
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['menu'] = menu # добавляем к словарю контекста ключ 'menu' а в качестве значения передаём список menu
        #context['title'] = 'Категория - ' + str(context['posts'][0].cat) # 'context' - это словарь, 'post' - это список, который берется из переменной context_object_name, который мы объявили в теле класса WomenCategory, далее берется первый элемент в этом списке и запрашивается 'cat'
        #context['cat_selected'] = context['posts'][0].cat_id # этот 'post' (представляет собой список) берется из переменной context_object_name, который мы объявили в теле класса WomenCategory, далее берется первый элемент в этом списке и запрашивается 'cat_id', т.е. идентификатор категории
        c = Category.objects.get(slug=self.kwargs['cat_slug']) # пишем это для оптимизации sql-запросов, для того, чтобы вместо двух дублирующх запросов, которые мы делали ниже, мы выполняли оди запрос тут, а потом просто вызывали его значения
        c_def = self.get_user_context(title='Категория - ' + str(c.name), # вот этот зпрос оптимизировали category.name, а было context['post'][0].cat
                                      cat_selected=c.pk) # вот этот зпрос оптимизировали category.pk , а было context['post'][0].cat_id
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    '''
    определяем класс по отображению формы регистрации нового пользователя
    '''
    form_class = RegisterUserForm # эта наша форма, которую мы создали в файле всех форм forms.py
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        '''
        если всё данные введены коректно, авторизуем пользователя сразу после регистрации его на сайте
        '''
        user = form.save()
        login(self.request, user) # автризацию выполняет эта функция login
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    '''
    авторизация пользователя
    '''
    form_class = LoginUserForm # здесь мы указываем нашу форму, которую мы прописали в forms.py
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация") # тут мы прнимаем таблицу, котормую мы создли в классе-примяси DataMixin и помещаем её содержимое в переменную c_def
        return dict(list(context.items()) + list(c_def.items())) # тут мы объеденяем два словаря в один единый, для того, чтобы передаеть его в 'women/login.html' ( а он принимает только 1 арумент )

    def get_success_url(self):
        '''
        если авторизация прошла успешно, то пользователя лениво перекидывает на страницу home
        '''
        return reverse_lazy('home')


def logout_user(request):
    '''
    создаём функция выхода из аккаунта пользователя ( класс нам тут не нужен )
    '''
    logout(request) # а это сама функция которая совершает выход из аккаунта
    return redirect('login')
