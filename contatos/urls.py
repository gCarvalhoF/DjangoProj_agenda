from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('busca/', views.search, name='busca'),
    path('<int:contato_id>', views.details, name='detalhes'),
    path('edit-contact/', views.edit_contact, name='edit-contact'),
    path('edit-contact/<int:contact_id>',
         views.edit_contact, name='edit-contact'),
]
