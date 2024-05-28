from django.shortcuts import get_object_or_404, render
from django.core.serializers import serialize
from .models import Ocorrencia

# def map_view(request):
#     ocorrencias = Ocorrencia.objects.all()
#     return render(request, 'core/map.html', {'ocorrencias': ocorrencias})

def map_view(request):
    ocorrencias = Ocorrencia.objects.all()
    ocorrencias_json = serialize('json', ocorrencias, use_natural_foreign_keys=True)
    return render(request, 'core/map.html', {'ocorrencias': ocorrencias_json})

def ocorrencia_detail_view(request, pk):
    ocorrencia = get_object_or_404(Ocorrencia, pk=pk)
    return render(request, 'core/ocorrencia_detail.html', {'ocorrencia': ocorrencia})
