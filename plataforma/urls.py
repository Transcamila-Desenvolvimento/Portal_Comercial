from django.urls import path
from . import views

urlpatterns = [
    path('', views.plataforma, name="plataforma")
]
