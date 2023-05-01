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
    path('display/',views.display_dataset,name='display'),
    path('update_d/',views.update_d,name='update_d'),
    path('delete_vid/', views.delete_vid, name='delete_vid'),
    path('check/',views.choice_d,name="check"),
    path('update/', views.update, name='update'),
    #path('update_dataset/',views.update_dataset,name='update_dataset'),
    path('get_dataset_info/',views.get_dataset_info,name='get_dataset_info')
]