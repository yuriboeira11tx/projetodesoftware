from django.urls import path
from . import views

urlpatterns = [
    path('', views.map, name='mapa'),
    path('ocorrencia/<int:pk>/', views.detalhe_ocorrencia, name='detalhe_ocorrencia'),
    path('ocorrencia/registro/', views.registro_ocorrencia, name='registro_ocorrencia'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('logout/', views.clogout, name='logout'),
]
