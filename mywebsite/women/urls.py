from .views import *
from django.urls import path
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', WomenHome.as_view(), name='home' ),
    path('about/', AboutThisWebSite.as_view(), name='about' ),
    path('add_page/', AddPage.as_view(), name='add_page' ),
    path('contact/', ContactFromView.as_view(), name='contact' ),
    path('login/', LoginUser.as_view(), name='login' ),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post' ),
    path('cats/<slug:cat_slug>/', WomenCategory.as_view(), name='category' ),
]