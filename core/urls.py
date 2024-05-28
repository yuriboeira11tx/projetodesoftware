from django.urls import path
from . import views

urlpatterns = [
    path('', views.map_view, name='map_view'),
    path('ocorrencia/<int:pk>/', views.ocorrencia_detail_view, name='ocorrencia_detail'),
    path('register-occurrence/', views.register_occurrence, name='register_occurrence'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.clogout, name='logout'),
]
