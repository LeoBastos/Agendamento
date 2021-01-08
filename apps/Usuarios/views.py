from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from valida import *
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required

def cadastro(request):
    """ Sessão de Cadastro """
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        
        if len(senha) < 6:
            messages.error(request, 'A Senha deve ter mais do que 6 Caracteres')            
            return redirect('cadastro')

        if validacampo(nome):           
            messages.error(request, 'O campo nome não pode ficar em branco')            
            return redirect('cadastro')

        if validacampo(email):            
            messages.error(request, 'O campo email não pode ficar em branco')            
            return redirect('cadastro')

        if validasenha(senha, senha2):
            messages.error(request, 'As senhas precisam ser iguais')            
            return redirect('cadastro')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este Email já possui esta sendo utilizado')            
            return redirect('cadastro')

        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Usuário já possui esta sendo utilizado')            
            return redirect('cadastro')

        try:
            validate_email(email)
        except:
            messages.error(request, 'Email Inválido')            
            return redirect('cadastro')

        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Cadastrado Realizado com Sucesso')            
        return redirect('login')
    else:
        return render(request,'usuarios/cadastro.html')


def login(request):
    """ Sessão de Login """    
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']

        if email == "" or senha == "":
            messages.error(request, 'Os campos email e senha não podem ficar em branco')                        
            return redirect('login')  
        
        if email != email:
            messages.error(request, 'Email não Cadastrado')                        
            return redirect('login')

        if senha != senha:
            messages.error(request, 'Senha inválida')                        
            return redirect('login')  


        if senhainvalida(senha):
            messages.error(request, 'Senha Inválida')
            return redirect('login')       

        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Login realizado com sucesso')               
                return redirect('index')
        else:
            messages.error(request, 'Email ou Senha Inválidos')
            return redirect('login')
    return render(request, 'usuarios/login.html')

@login_required(redirect_field_name='login')
def dashboard(request):
    """ Dashboard do Usuários - Em Construção """
    return render(request, 'usuarios/dashboard.html')


def logout (request):
    """ Sessão de Logout """
    auth.logout(request)
    messages.success(request, 'Deslogado com Sucesso')
    return redirect('login')



