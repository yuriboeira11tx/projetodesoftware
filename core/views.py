from django.shortcuts import get_object_or_404, render, redirect
from django.core.serializers import serialize
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from .models import Ocorrencia


def map_view(request):
    ocorrencias = Ocorrencia.objects.all()
    ocorrencias_json = serialize('json', ocorrencias, use_natural_foreign_keys=True)
    return render(request, 'core/map.html', {'ocorrencias': ocorrencias_json})

def ocorrencia_detail_view(request, pk):
    ocorrencia = get_object_or_404(Ocorrencia, pk=pk)
    return render(request, 'core/ocorrencia_detail.html', {'ocorrencia': ocorrencia})

def register_occurrence(request):
    if request.method == 'POST':
        form = OcorrenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('map_view')
    else:
        form = OcorrenciaForm()
    return render(request, 'register_occurrence.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('map_view')
        else:
            pass

    return render(request, 'core/login.html')

def clogout(request):
    logout(request)
    return redirect('map_view')

def cadastro_view(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        if User.objects.filter(username=username).exists():
            pass
        else:
            user = User.objects.create_user(username=username, password=senha)
            user.first_name = nome
            user.save()
            return redirect('login')
    
    return render(request, 'core/cadastro.html')
