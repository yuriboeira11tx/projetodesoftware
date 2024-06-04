from django.shortcuts import get_object_or_404, render, redirect
from django.core.serializers import serialize
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import Imagem, Ocorrencia
from datetime import datetime

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

def minhas_ocorrencias(request):
    if request.user.is_authenticated:
        ocorrencias = Ocorrencia.objects.filter(mergulhador=request.user)
        return render(request, 'core/ocorrencias_usuario.html', {'ocorrencias': ocorrencias})
    else:
        return render(request, 'core/ocorrencias_usuario.html', {})

def detalhe_ocorrencia(request, pk):
    ocorrencia = get_object_or_404(Ocorrencia, pk=pk)
    imagens = Imagem.objects.filter(ocorrencia=ocorrencia)
    return render(request, 'core/ocorrencia_detail.html', {'ocorrencia': ocorrencia, 'imagens': imagens})

def excluir_ocorrencia(request, pk):
    ocorrencia = get_object_or_404(Ocorrencia, pk=pk)
    if request.method == 'POST':
        imagens = Imagem.objects.filter(ocorrencia=ocorrencia)
        for imagem in imagens:
            imagem.delete()
        
        ocorrencia.delete()
        messages.success(request, 'Ocorrência excluída com sucesso.')
        ocorrencias = Ocorrencia.objects.filter(mergulhador=request.user)
        return render(request, 'core/ocorrencias_usuario.html', {'ocorrencias': ocorrencias})
    
    ocorrencias = Ocorrencia.objects.filter(mergulhador=request.user)
    return render(request, 'core/ocorrencias_usuario.html', {'ocorrencias': ocorrencias})

def editar_ocorrencia(request, pk):
    ocorrencia = get_object_or_404(Ocorrencia, pk=pk)
    imagens = Imagem.objects.filter(ocorrencia=ocorrencia)

    if request.method == 'POST':
        profundidade = request.POST.get('profundidade')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        visibilidade = request.POST.get('visibilidade')
        temperatura_agua = request.POST.get('temperatura_agua')
        quantidade = request.POST.get('quantidade')
        data_str = request.POST.get('data')
        especie = request.POST.get('especie')

        if data_str:
            try:
                data = datetime.strptime(data_str, '%Y-%m-%d').date()
            except ValueError:
                return HttpResponse('A data fornecida é inválida.')
        else:
            data = None

        profundidade = float(profundidade.replace(',', '.')) if profundidade else None
        latitude = float(latitude.replace(',', '.')) if latitude else None
        longitude = float(longitude.replace(',', '.')) if longitude else None
        visibilidade = float(visibilidade.replace(',', '.')) if visibilidade else None
        temperatura_agua = float(temperatura_agua.replace(',', '.')) if temperatura_agua else None
        quantidade = int(quantidade) if quantidade else None
        
        ocorrencia.profundidade = profundidade
        ocorrencia.latitude = latitude
        ocorrencia.longitude = longitude
        ocorrencia.visibilidade = visibilidade
        ocorrencia.temperatura_agua = temperatura_agua
        ocorrencia.quantidade = quantidade
        ocorrencia.data = data
        ocorrencia.especie = especie
        
        ocorrencia.save()
        
        novas_imagens = request.FILES.getlist('imagens')
        for imagem in novas_imagens:
            Imagem.objects.create(ocorrencia=ocorrencia, imagem=imagem)
        
        return redirect('detalhe_ocorrencia', pk=pk)
    
    return render(request, 'core/editar_ocorrencia.html', {'ocorrencia': ocorrencia, 'imagens': imagens})

def remover_imagem(request, pk, imagem_pk):
    ocorrencia = get_object_or_404(Ocorrencia, pk=pk)
    imagem = get_object_or_404(Imagem, pk=imagem_pk)
    
    if imagem.ocorrencia != ocorrencia:
        return JsonResponse({'error': 'Essa imagem não pertence à ocorrência.'}, status=400)
    
    imagem.delete()
    
    return redirect('detalhe_ocorrencia', pk=pk)

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
