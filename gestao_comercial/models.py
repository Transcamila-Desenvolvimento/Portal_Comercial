from django.db import models
from django.db.models import Max
from django.utils import timezone

class Proposta(models.Model):
    # Choices para TIPO_SERVICO
    TIPO_TRANSPORTE = 'transporte'
    TIPO_ARMAZEM = 'armazem'
    
    TIPO_SERVICO_CHOICES = [
        (TIPO_TRANSPORTE, 'TRANSPORTE'),
        (TIPO_ARMAZEM, 'ARMAZÉM'),
    ]

    # Choices para STATUS_PROPOSTA
    STATUS_APROVADA = 'aprovada'
    STATUS_PENDENTE = 'pendente'
    STATUS_REJEITADA = 'rejeitada'
    
    STATUS_CHOICES = [
        (STATUS_APROVADA, 'APROVADA'),
        (STATUS_PENDENTE, 'PENDENTE'),
        (STATUS_REJEITADA, 'REJEITADA'),
    ]

    numero_proposta = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Número da Proposta",
        editable=False
    )
    data_emissao = models.DateField(
        auto_now_add=True,
        verbose_name="Data de Emissão"
    )
    cliente = models.CharField(
        max_length=50,
        verbose_name="Cliente"
    )
    tipo_servico = models.CharField(
        max_length=10,
        choices=TIPO_SERVICO_CHOICES,
        default=TIPO_TRANSPORTE,
        verbose_name="Tipo de Serviço"
    )
    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor Total (R$)"
    )
    status_proposta = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDENTE,
        verbose_name="Status"
    )

    def save(self, *args, **kwargs):
        if not self.numero_proposta:
            # Encontra a última proposta
            ultima_proposta = Proposta.objects.aggregate(
                max_numero=Max('numero_proposta')
            )
            
            if ultima_proposta['max_numero']:
                # Converte para inteiro e incrementa
                ultimo_numero = int(ultima_proposta['max_numero'])
                novo_numero = ultimo_numero + 1
            else:
                # Primeira proposta do sistema
                novo_numero = 1
            
            # Formata com 4 dígitos (0001, 0002...)
            self.numero_proposta = f"{novo_numero:04d}"
        
        super().save(*args, **kwargs)

    def valor_formatado(self):
        """Formata o valor como 10.000,00 (padrão brasileiro)"""
        return f"{self.valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def data_emissao_formatada(self):
        """Formata a data como DD/MM/AAAA"""
        return self.data_emissao.strftime("%d/%m/%Y")

    def __str__(self):
        return f"Proposta {self.numero_proposta} - {self.cliente}"

    class Meta:
        verbose_name = "Proposta"
        verbose_name_plural = "Propostas"
        ordering = ['-data_emissao']  # Ordena por data decrescente