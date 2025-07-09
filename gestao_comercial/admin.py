from django.contrib import admin
from .models import Proposta

class PropostaAdmin(admin.ModelAdmin):
    list_display = (
        'numero_proposta',
        'cliente',
        'tipo_servico',
        'valor_formatado',
        'data_emissao_formatada',
        'status_proposta'
    )
    list_filter = ('tipo_servico', 'status_proposta', 'data_emissao')
    search_fields = ('numero_proposta', 'cliente')
    date_hierarchy = 'data_emissao'

    # Campos personalizados para exibição
    def valor_formatado(self, obj):
        return obj.valor_formatado()
    valor_formatado.admin_order_field = 'valor_total'  # Permite ordenação pelo valor original
    valor_formatado.short_description = 'Valor Total (R$)'

    def data_emissao_formatada(self, obj):
        return obj.data_emissao_formatada()
    data_emissao_formatada.admin_order_field = 'data_emissao'  # Ordenação pela data original
    data_emissao_formatada.short_description = 'Data de Emissão'

admin.site.register(Proposta, PropostaAdmin)