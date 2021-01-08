from django.contrib import admin
from .models import Cliente, Serviço, Pagamento, Modelo, Agendamento

class ClienteAdmin(admin.ModelAdmin):
    search_fields = ('nome', 'celular', 'cpf', 'status')
    list_display = ('id', 'nome', 'celular', 'cpf','status')
    list_display_links = ('id', 'nome', 'celular', 'cpf')
    list_filter = ('nome','cpf','status')
    list_editable = ('status',)
    list_per_page = 10

class ServiçoAdmin(admin.ModelAdmin):
    list_display = ( 'id','servico',)
    list_display_links = ('servico',)
    list_filter = ('servico',)
    list_per_page = 10

class PagamentoAdmin(admin.ModelAdmin):
    list_display = ( 'id','pagamento',)
    list_display_links = ('pagamento',)
    list_filter = ('pagamento',)
    list_per_page = 10

class ModeloAdmin(admin.ModelAdmin):
    list_display = ( 'modelo',)
    list_display_links = ('modelo',)
    list_filter = ('modelo',)
    list_per_page = 10


class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'data','horainicial', 'horafinal', 'cliente', 'servico')
    list_display_links = ('data','horainicial', 'horafinal', 'cliente', 'servico')
    list_filter = ('data','horainicial', 'horafinal', 'cliente')
    list_per_page = 10


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Serviço, ServiçoAdmin)
admin.site.register(Pagamento, PagamentoAdmin)
admin.site.register(Modelo, ModeloAdmin)
admin.site.register(Agendamento, AgendamentoAdmin)
