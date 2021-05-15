from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('wish_items/create', views.create),
    path('wish_items/add', views.add),
    path('wish_items/<int:id>', views.item),
    path('wish_items/<int:id>/get', views.getItem),
    path('remove/<int:id>', views.remove),
    path('delete/<int:id>', views.delete)
]