from django.shortcuts import get_object_or_404, render, redirect
from django.core.serializers import serialize
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Imagem, Ocorrencia

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

def cadastro(request):
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

def map(request):
    ocorrencias = Ocorrencia.objects.all()
    ocorrencias_json = serialize('json', ocorrencias, use_natural_foreign_keys=True)
    return render(request, 'core/map.html', {'ocorrencias': ocorrencias_json})

def detalhe_ocorrencia(request, pk):
    ocorrencia = get_object_or_404(Ocorrencia, pk=pk)
    return render(request, 'core/ocorrencia_detail.html', {'ocorrencia': ocorrencia})

@login_required
def registro_ocorrencia(request):
    if request.method == 'POST':
        try:
            profundidade = request.POST.get('profundidade')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            visibilidade = request.POST.get('visibilidade')
            temperatura_agua = request.POST.get('temperatura_agua')
            quantidade = request.POST.get('quantidade')
            data = request.POST.get('data')
            especie = request.POST.get('especie')
            imagens = request.FILES.getlist('imagens')

            ocorrencia = Ocorrencia.objects.create(
                mergulhador=request.user,
                profundidade=profundidade,
                latitude=latitude,
                longitude=longitude,
                visibilidade=visibilidade,
                temperatura_agua=temperatura_agua,
                quantidade=quantidade,
                data=data,
                especie=especie
            )

            for image in imagens:
                Imagem.objects.create(ocorrencia=ocorrencia, imagem=image)

            return redirect('mapa')
        except Exception as e:
            error_message = str(e)
            ocorrencias = Ocorrencia.objects.all()
            ocorrencias_json = serialize('json', ocorrencias, use_natural_foreign_keys=True)
            return render(request, 'core/map.html', {'ocorrencias': ocorrencias_json, 'error_message': error_message})

    return render(request, 'core/map.html')
