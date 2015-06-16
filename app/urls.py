from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'soccer/', views.soccer, name='soccer'),
        url(r'complete/', views.complete, name='complete'),
        url(r'login/', views.user_login, name='user_login'),
        url(r'profile/', views.profile, name='profile'),
        url(r'math/', views.math, name='math'),
        url(r'rappers/', views.rappers),
        url(r'movies/', views.movies),
        url(r'musicians/', views.musicians),
        url(r'colors/', views.colors),
        url(r'places/', views.places),
        url(r'numbers/', views.numbers),
        url(r'data/', views.data, name='data'),
        )