from django.urls import path
from . import views

urlpatterns = [
    path('propostas/', views.gestao_comercial, name="propostas"),
    path('propostas/incluir', views.incluir_proposta, name="incluir_proposta"),
]
