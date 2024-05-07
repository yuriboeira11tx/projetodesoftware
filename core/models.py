from django.db import models
from django.contrib.auth.models import User

class Imagem(models.Model):
    imagem = models.ImageField(upload_to='imagens/')
    
    
class Ocorrencia(models.Model):
    mergulhador = models.ForeignKey(User, on_delete=models.CASCADE)
    profundidade = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    visibilidade = models.FloatField()
    temperatura_agua = models.FloatField()
    quantidade = models.IntegerField()
    data = models.DateField()
    imagens = models.ManyToManyField(Imagem, blank=True)
    especie = models.CharField(max_length=100)

    def __str__(self):
        return f"Coleta de {self.mergulhador.username} em {self.data}"
