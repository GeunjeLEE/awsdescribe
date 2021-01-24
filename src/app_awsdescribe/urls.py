from django.urls import path

from . import views

app_name = 'app_awsdescribe'
urlpatterns = [
    path('', views.index, name='index'),
    path('environment_list/', views.environment_list, name='environment_list'),
    path('ec2_list/', views.ec2_list, name='ec2_list'),
    path('user_list/', views.user_list, name='user_list'),
    path('data_batch/', views.data_batch, name='data_batch'),
    path('sync/', views.sync, name='sync'),
]