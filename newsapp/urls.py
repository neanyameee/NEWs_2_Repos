from django.urls import path
from django.views.i18n import set_language as django_set_language
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('preferences/', views.preferences, name='preferences'),
    path('theme/<str:theme>/', views.set_theme, name='set_theme'),
    path('language/<str:language>/', views.set_language, name='set_language'),
    path('i18n/setlang/', django_set_language, name='set_language_django'),
]