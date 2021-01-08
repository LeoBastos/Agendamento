from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from .models import Cliente, Serviço, Agendamento,Modelo, Pagamento
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Value
from django.db.models.functions import Concat
from valida import *
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime, date, timedelta
from django.contrib.auth.decorators import login_required


""" SEÇÃO CLIENTES """
@login_required(login_url='login')
def index(request):
    """ Exibe a lista de clientes e Agendamentos na index """       
    today = datetime.now()    
    
    dia_semana = datetime.today()
    dias = ('Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo')
    dias = dias[dia_semana.weekday()]

    agendamentos = Agendamento.objects.all().filter(data=datetime.date(today)).order_by('horainicial')
    clientes = Cliente.objects.order_by('-id').filter(status=True)

    dados = {       
        'agendamentos': agendamentos,
        'clientes': clientes,
        'dias': dias,
        'dia_semana': dia_semana,
    }   
    
    return render(request,'agenda/index.html', dados)


@login_required(login_url='login')
def vercliente(request, cliente_id):
    """ Exibe Cliente Único Pelo ID """
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    agendamento = Agendamento.objects.all()
    
    cliente_lista = {
        'cliente': cliente,
        'agendamento': agendamento,
    }
    return render(request, 'cliente/ver_cliente.html', cliente_lista)


@login_required(login_url='login')
def buscar(request):
    """Metodo para Buscar Cliente por Nome"""
    buscar = request.GET['buscar']     

    lista_cliente = Cliente.objects.filter(Q(nome__icontains=buscar) | Q(celular__icontains=buscar) | Q(cpf__icontains=buscar))
    #lista_agendamento = Agendamento.objects.filter(Q(cliente__icontains=buscar) | Q(servico__icontains=buscar) | Q(pagamento__icontains=buscar) )
    
            
    dados = {
        'clientes': lista_cliente,
        #'agendamento': lista_agendamento,
              
    }
    
    return render(request, 'agenda/buscar.html', dados)


@login_required(login_url='login')
def cliente(request):
    """ Listar Cliente """
    clientes = Cliente.objects.order_by('-id').filter(status=True)
    
    paginator = Paginator(clientes, 5)
    page = request.GET.get('page')
    clientes_pagina = paginator.get_page(page)

    dados = {
        'clientes': clientes_pagina
    }
    
    return render(request,'cliente/cliente.html', dados)


@login_required(login_url='login')
def cadcli(request):
    """ Cadastrar Cliente """
    if request.method == 'POST':        
        nome = request.POST['nome']        
        cpf = request.POST['cpf']
        email = request.POST['email']
        celular = request.POST['celular']
           
        if Cliente.objects.filter(email=email).exists():
            messages.error(request, 'Este Email já possui Cadastro')            
            return redirect('cliente')

        if Cliente.objects.filter(nome=nome).exists():
            messages.error(request, 'Nome já possui Cadastro')            
            return redirect('cliente')

        if Cliente.objects.filter(cpf=cpf).exists():
            messages.error(request, 'Este Cpf já possui cadastro')            
            return redirect('cliente')

        if len(cpf) < 11:
            messages.error(request, 'CPF Incompleto ou inválido')
            return redirect('cliente')

        if len(celular) < 11:
            messages.error(request, 'Celular Precisa de 11 Caracteres')
            return redirect('cliente')       
        
        
        if len(nome) < 3:
            messages.error(request, 'Nome Deve ter mais do que 3 Caractéres')
            return redirect('cliente')

        if validacampo(nome):           
            messages.error(request, 'O Campo nome não pode ficar em branco')
            return redirect('cliente')
        
        
            
        else:
            #user = get_object_or_404(Cliente, pk=request.user.id)
            cliente = Cliente.objects.create(nome=nome,cpf=cpf, email=email, celular=celular)
            
            cliente.save()
            messages.success(request, 'Cliente Cadastrado com Sucesso')
            return redirect('cliente')
    else:        
        return redirect('cliente')


@login_required(login_url='login')
def deletar(request, cliente_id):
    """ Deletar Cliente """
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    cliente.delete()
    return redirect('cliente')


@login_required(login_url='login')
def editar(request, cliente_id):
    """ Lógica para captura do objeto para editar """
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    cliente_edita = { 'cliente': cliente }
    return render(request, 'cliente/editar.html', cliente_edita)


@login_required(login_url='login')
def update_cliente(request):
    """ Update Cliente """        
    if request.method == 'POST':
        cliente_id = request.POST['cliente_id']
        c = Cliente.objects.get(pk=cliente_id)
        #c.status = request.POST['status']
        c.nome = request.POST['nome']
        c.cpf = request.POST['cpf']       
        c.email = request.POST['email']
        c.celular = request.POST['celular']               
                
        c.save()
        return redirect('cliente')
    else:
        return render(request, 'cliente/editar.html')


""" SEÇÃO DE SERVIÇOS """

@login_required(login_url='login')
def servico(request):
    """ Listagem dos Serviços """
    servicos = Serviço.objects.order_by('id')
    
    paginator = Paginator(servicos, 10)
    page = request.GET.get('page')
    servicos_pagina = paginator.get_page(page)

    dados = {
        'servicos': servicos_pagina
    }

    return render(request,'servico/servico.html', dados)
   

@login_required(login_url='login')
def cadserv(request):
    """ Cadastrar um Serviço """
    if request.method == 'POST':        
        servico = request.POST['servico']
        

        if Serviço.objects.filter(servico=servico).exists():
            messages.error(request, 'Este Serviço já possui Cadastro')            
            return redirect('servico')

        else:
            servico = Serviço.objects.create(servico=servico)
            servico.save()
            messages.success(request, 'Servico Cadastrado com Sucesso')
            return redirect('servico')


@login_required(login_url='login')
def deletarserv(request, servico_id):
    """ Deletar Serviços """
    servico = get_object_or_404(Serviço, pk=servico_id)
    servico.delete()
    return redirect('servico')


@login_required(login_url='login')
def editarserv(request, servico_id):
    """ Lógica para construir objeto para Editar """
    servico = get_object_or_404(Serviço, pk=servico_id)
    servico_edita = { 'servico': servico }
    return render(request, 'servico/editarserv.html', servico_edita)


@login_required(login_url='login')
def update_servico(request):
    """ Update Serviços """
    if request.method == 'POST':
        servico_id = request.POST['servico_id']
        s = Serviço.objects.get(pk=servico_id)
        s.servico = request.POST['servico']        
        s.save()
        return redirect('servico')


""" SEÇÃO AGENDA/AGENDAMENTOS """

@login_required(login_url='login')
def agenda(request):
    """Construção do Cadastro e Visualização da Agenda """
    agendamentos = Agendamento.objects.order_by('data')
    servicos = Serviço.objects.order_by('-id')
    clientes = Cliente.objects.order_by('-id')
    pagamentos = Pagamento.objects.order_by('-id')
    modelos = Modelo.objects.order_by('-id')    
    
    paginator = Paginator(agendamentos, 5)
    page = request.GET.get('page')
    agendamentos_pagina = paginator.get_page(page)

    dados = {
        'agendamentos': agendamentos_pagina,
        'servicos': servicos,
        'clientes': clientes,
        'modelos': modelos,
        'pagamentos': pagamentos
    }   
    
    return render(request,'agenda/agenda.html', dados)


@login_required(login_url='login')
def cadagenda(request):
    """ Cadastrar uma Data na Agenda """   
    servico = Serviço.objects.order_by('-id')
    cliente = Cliente.objects.order_by('-id')
    pagamento = Pagamento.objects.order_by('pagamento')
    modelo = Modelo.objects.order_by('-modelo')  

    if request.method == 'POST':                
        data = request.POST['data']
        servico = request.POST['servico']
        horainicial = request.POST['horainicial']
        horafinal = request.POST['horafinal']
        cliente = request.POST['cliente']
        modelo = request.POST['modelo']
        pagamento = request.POST['pagamento']
       
        #data_atual = datetime.today()
        data_atual = datetime.today()
        data_atual = datetime.strftime(data_atual, '%Y-%m-%d')
        #data = datetime.strptime(data, '%Y-%m-%d')
        #intervalo = timedelta(minutes=30)
                      
       
        if data == data_atual and data > data_atual:
                       
            messages.success(request, 'Agendamento Efetuado com Sucesso')           
            return redirect('index')

        if data < data_atual:            
            messages.error(request, 'Data de Cadastro não pode ser anterior ao dia atual')
            return redirect('index')
        
        if horafinal < horainicial:            
            messages.error(request, 'Hora Final não pode ser menor que a Hora Inicial')
            return redirect('index')

        if Agendamento.objects.filter(horainicial=horainicial).exists() and data == data_atual:
            messages.error(request, 'Já Existe um Agendamento neste Horário')
            return redirect('index') 

        if Agendamento.objects.filter(horainicial=horainicial).exists() and horainicial > 45:
            messages.error(request, 'Já Existe um Agendamento neste Horário')
            return redirect('index') 
        
        else:               
            agenda = Agendamento.objects.create(data=data,servico=Serviço.objects.get(id=servico),horainicial=horainicial,horafinal=horafinal, cliente=Cliente.objects.get(nome=cliente),modelo=Modelo.objects.get(modelo=modelo),pagamento=Pagamento.objects.get(pagamento=pagamento)) 
            agenda.save()
            messages.success(request, 'agendamento Cadastrado com Sucesso')
            return redirect('agenda')


@login_required(login_url='login')
def deletaragenda(request, agenda_id):
    """ Deletar Agenda """
    agenda = get_object_or_404(Agendamento, pk=agenda_id)
    agenda.delete()
    return redirect('agenda')


@login_required(login_url='login')
def editaragenda(request, agendamento_id):
    """ Lógica para construir objeto para Editar """
    agendamento = get_object_or_404(Agendamento, pk=agendamento_id)
    agendamento_edita = { 'agendamento': agendamento }
    return render(request, 'agenda/editaragenda.html', agendamento_edita)


@login_required(login_url='login')
def update_agenda(request):
    """ Update Agenda """
    if request.method == 'POST':
        
        s = Serviço.objects.all()
        c = Cliente.objects.all()
        m = Modelo.objects.all()
        p = Pagamento.objects.all()  

        agendamento_id = request.POST['agendamento_id']
        a = Agendamento.objects.get(pk=agendamento_id)

        s.servico = request.POST['servico']
        a.data = request.POST['data']
        a.horainicial = request.POST['horainicial']
        a.horafinal = request.POST['horafinal']         
        c.cliente = request.POST['cliente']
        m.pagamento = request.POST['pagamento']               
        p.forma = request.POST['modelo']       
      
        a.save()
        return redirect('agenda')
    else:
        return render(request, 'editaragenda.html')