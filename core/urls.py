from django.urls import path
from . import views

urlpatterns = [
    path('', views.map_view, name='map_view'),
    path('ocorrencia/<int:pk>/', views.ocorrencia_detail_view, name='ocorrencia_detail'),
]
