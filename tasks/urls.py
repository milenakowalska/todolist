from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('contact', views.contact, name='contact'),
    path('create_list', views.create_list, name='create_list'),
    path('active_lists', views.active_lists, name='active_lists'),
    path('archived_lists', views.archived_lists, name='archived_lists'),
    path('list/<int:list_id>', views.list_page, name='list_page'),
    path('change_background', views.change_background, name='change_background')
]