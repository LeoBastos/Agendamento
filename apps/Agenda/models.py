from django.db import models
from django.conf import settings
from datetime import datetime


class Agendamento(models.Model):
    data = models.DateField(default=datetime.now)
    horainicial = models.TimeField()
    horafinal = models.TimeField()
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE,related_name='clienteagendamento')
    servico = models.ForeignKey('Serviço', on_delete=models.CASCADE, related_name='servicoagendamento')
    modelo = models.ForeignKey('Modelo', on_delete=models.CASCADE, related_name='modeloagendamento')
    pagamento = models.ForeignKey('Pagamento', on_delete=models.CASCADE, blank=True, null=True)
    


class Cliente(models.Model):
    nome = models.CharField(max_length=30, unique=True)    
    cpf = models.CharField(max_length=11, unique=True)    
    email = models.CharField(max_length=60, unique=True)
    celular = models.CharField(max_length=11)    
    dataCadastro = models.DateField(default=datetime.now, blank=True)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome
        

class Serviço(models.Model):
    servico = models.CharField(max_length=30, unique=True)   
    
    def __str__(self):
        return self.servico


class Modelo(models.Model):
    Modelo_CHOICES = (
        ("Plano de Saude", "Plano"),
        ("Particular", "Particular"),
    )
    modelo = models.CharField(max_length=16, choices=Modelo_CHOICES, blank=False, null=False)

    def __str__(self):
        return self.modelo


class Pagamento(models.Model):
    Pagamento_CHOICES = (
        ("Convenio", "Convenio"),
        ("Cartão - Debito", "Cartao de Debito"),
        ("Cartão - Credito", "Cartao de Credito"),
        ("Dinheiro", "Dinheiro"),
    )
    pagamento = models.CharField(max_length=20, choices=Pagamento_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.pagamento




   



   
