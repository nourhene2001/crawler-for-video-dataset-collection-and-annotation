from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns=[
    path('search/',views.search, name='search'),
    path('check/',views.check,name='check'),
    path('accounts/login/', views.login, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    path('signup/', views.register, name='signup'),

]