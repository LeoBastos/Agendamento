from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),   
    path('buscar', views.buscar, name='buscar'),     
    
    path('cliente', views.cliente, name='cliente'),
    path('vercliente/<int:cliente_id>', views.vercliente, name='vercliente'),
    path('cliente/cadastrar', views.cadcli, name='cadastrar'),
    path('deletar/<int:cliente_id>', views.deletar, name='deletar'),
    path('editar/<int:cliente_id>', views.editar, name='editar'),
    path('update_cliente', views.update_cliente, name='update_cliente'),

    path('servico', views.servico, name='servico'),
    path('servico/cadastrar', views.cadserv, name='cadastrar_servico'),
    path('deletarserv/<int:servico_id>', views.deletarserv, name='deletarserv'),
    path('editarserv/<int:servico_id>', views.editarserv, name='editarserv'),
    path('update_servico', views.update_servico, name='update_servico'),  

    path('agenda', views.agenda, name='agenda'),
    path('agenda/cadastrar', views.cadagenda, name='cadastrar_agenda'),
    path('deletaragenda/<int:agenda_id>', views.deletaragenda, name='deletaragenda'),
    path('editaragenda/<int:agendamento_id>', views.editaragenda, name='editaragenda'),
    path('update_agenda', views.update_agenda, name='update_agenda'),     
]