from django.urls import path
from . import views

urlpatterns = [
    path('data-center/', views.data_center, name='data_center'),
]
