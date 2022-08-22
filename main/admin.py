from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from.models import *


class MyUserAdmin(UserAdmin):
    model = Usuario
    list_display = ()
    list_filter = ()
    search_fields = ()
    ordering = ()
    filter_horizontal = ()
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nome_log',)}),
    )
admin.site.register(Usuario, MyUserAdmin)

# icons available in: https://materializecss.com/icons.html


############### SISTEMA ###################

class MaterialEventsAdmin(ModelAdmin):
    icon_name = 'event_note'
    fieldsets = (
        (None, {
            'fields': ('full_name', 'social_name', "birth_date",),
            'classes': ('wide',),
        }),

    )



class OperadorListAdmin(ModelAdmin):
    list_display = ('idk', 'nome_completo', 'data_nascimento', 'telefone', 'whatsapp', 'cpf', 'funcao_operador')
    list_editable = ('nome_completo', 'data_nascimento', 'telefone', 'whatsapp', 'cpf', 'funcao_operador',)
admin.site.register(Operador, OperadorListAdmin)



class MaquinarioListAdmin(ModelAdmin):
    list_display = ('idk', 'numero', 'nome', 'modelo', 'status', 'valor', 'data_aquisicao', 'tipo', 'descricao',)
    list_editable = ('nome', 'valor', 'descricao',)
admin.site.register(Maquinario, MaquinarioListAdmin)



class AviamentoListAdmin(ModelAdmin):
    list_display = ('idk', 'codigo', 'nome', 'produto', 'categoria', 'marca', 'fornecedor', 'valor', 'data_aquisicao', 'quantidade', 'descricao')
    list_editable = ('nome', 'produto', 'categoria', 'marca', 'fornecedor', 'valor', 'quantidade', 'descricao',)
admin.site.register(Aviamento, AviamentoListAdmin)



class ManutencaoListAdmin(ModelAdmin):
    list_display = ('idk', 'numero', 'nome', 'motivo', 'prestador_servico', 'data_envio', 'provavel_retorno',)
admin.site.register(Manutencao, ManutencaoListAdmin)



class BaixaListAdmin(ModelAdmin):
    list_display = ('idk', 'numero', 'nome',)
admin.site.register(Baixa, BaixaListAdmin)



class ProcessoListAdmin(ModelAdmin):
    list_display = ('idk', 'nome', 'operador_alocado', 'maquinario_alocado', 'aviamento_utilizado', 'tempo_execucao',)
    list_editable = ('nome', 'operador_alocado', 'maquinario_alocado', 'aviamento_utilizado', 'tempo_execucao',)
admin.site.register(Processo, ProcessoListAdmin)