from django.urls import path
from . import views

urlpatterns = [
    path('', views.map, name='mapa'),
    path('ocorrencia/<int:pk>/', views.detalhe_ocorrencia, name='detalhe_ocorrencia'),
    path('ocorrencia/<int:pk>/editar/', views.editar_ocorrencia, name='editar_ocorrencia'),
    path('ocorrencia/<int:pk>/excluir/', views.excluir_ocorrencia, name='excluir_ocorrencia'),
    path('ocorrencia/registro/', views.registro_ocorrencia, name='registro_ocorrencia'),
    path('minhas-ocorrencias/', views.minhas_ocorrencias, name='minhas_ocorrencias'),
    path('ocorrencia/<int:pk>/imagem/<int:imagem_pk>/remover/', views.remover_imagem, name='remover_imagem'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('logout/', views.clogout, name='logout'),
]
