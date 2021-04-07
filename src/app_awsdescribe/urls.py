from django.urls import path

from . import views

app_name = 'app_awsdescribe'
urlpatterns = [
    path('', views.index, name='index'),
    path('environment_list/', views.environment_list, name='environment_list'),
    path('ec2_list/', views.ec2_list, name='ec2_list'),
    path('user_list/', views.user_list, name='user_list'),
    path('data_batch/', views.data_batch, name='data_batch'),
    path('rds_cluster_list/', views.rds_cluster_list, name='rds_cluster_list'),
    path('sync/', views.sync, name='sync'),
    path('insert_account_info/', views.insert_account_info, name='insert_account_info'),
    path('update_account_info/', views.update_account_info, name='update_account_info'),
    path('delete_account_info/', views.delete_account_info, name='delete_account_info'),
    path('vpc_list/', views.vpc_list, name='vpc_list'),
    path('subnet_list/', views.subnet_list, name='subnet_list'),
    path('sg_list/', views.sg_list, name='sg_list'),
    path('ip_list/', views.ip_list, name='ip_list'),
    path('get_account_detail/', views.get_account_detail, name='get_account_detail'),
    path('get_account_information_for_modify/', views.get_account_information_for_modify, name='get_account_information_for_modify')

]