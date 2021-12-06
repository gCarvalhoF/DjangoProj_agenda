from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='index_login'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-contact/', views.create_contact, name='create-contact'),
    path('create-category/', views.create_category, name='create-category'),

]
