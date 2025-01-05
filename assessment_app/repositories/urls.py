from django.urls import path
from .views import repository_list

urlpatterns = [
    path('', repository_list, name='repository_list'),
]

