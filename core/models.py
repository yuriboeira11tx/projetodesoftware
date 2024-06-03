from django.db import models
from django.contrib.auth.models import User

class Ocorrencia(models.Model):
    CORAL_SOL = 'CS'
    PEIXE_LEAO = 'PL'
    
    ESPECIE_CHOICES = [
        (CORAL_SOL, 'Coral Sol'),
        (PEIXE_LEAO, 'Peixe Leão'),
    ]

    mergulhador = models.ForeignKey(User, on_delete=models.CASCADE)
    profundidade = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    visibilidade = models.FloatField()
    temperatura_agua = models.FloatField()
    quantidade = models.IntegerField()
    data = models.DateField()
    especie = models.CharField(max_length=2, choices=ESPECIE_CHOICES, default=CORAL_SOL)

    def __str__(self):
        return f"Coleta de {self.mergulhador.username} em {self.data}"


class Imagem(models.Model):
    ocorrencia = models.ForeignKey(Ocorrencia, on_delete=models.SET_NULL, null=True, blank=True)
    imagem = models.ImageField(upload_to='imagens/', blank=False, null=False)
