from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns=[
    path('search/',views.search, name='search'),
    #path('check/',views.check,name='check'),
    path('accounts/login/', views.login, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    path('signup/', views.register, name='signup'),
    path('main/',views.main,name='main'),
    path('create_d/',views.create_d,name='create_d'),
    path('update_d/',views.update_d,name='update_d'),
    path('check/',views.choice_d,name="check"),
    path('update_d/update/<str:name>/', views.update, name='update')

]