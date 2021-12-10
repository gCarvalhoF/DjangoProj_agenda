from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import ContatoForm, CategoriaForm
from contatos.models import Contato
from django.http import Http404

import re


def verify_pwd_strength(pwd):
    if not len(pwd) >= 8:
        return False, 'Senha fraca. Sua senha precisa conter pelo menos 8 caracteres'
    lowerRegex = re.compile(r'[a-z]+')
    upperRegex = re.compile(r'[A-Z]+')
    symbolsRegex = re.compile(r'\W+')
    numbersRegex = re.compile(r'[0-9]+')

    if not upperRegex.search(pwd) or not lowerRegex.search(pwd):
        return False, 'Senha fraca. Sua senha precisa conter caracteres minúsculos e maiúsculos.'
    elif not symbolsRegex.search(pwd):
        return False, 'Senha fraca. Sua senha precisa conter caracteres especiais'
    elif not numbersRegex.search(pwd):
        return False, 'Senha fraca. Sua senha precisa conter números'
    else:
        return True, 'Senha forte!'


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválido(s).')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Logado com sucesso!')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    messages.info(request, 'Deslogado com sucesso!')
    return redirect('index')


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')

    email = request.POST.get('email')
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not email or not nome or not sobrenome or not usuario or not senha or not senha2:
        messages.error(request, 'Nenhum campo pode estar vazio!')
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido.')
        return render(request, 'accounts/register.html')

    if senha != senha2:
        messages.error(request, 'As senhas digitadas devem ser iguais')
        return render(request, 'accounts/register.html')

    if not verify_pwd_strength(senha)[0]:
        message = str(verify_pwd_strength(senha)[1])

        messages.error(request, message)
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Nome de usuário já foi cadastrado antes.')
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email já foi cadastrado antes.')
        return render(request, 'accounts/register.html')

    messages.success(request, 'Registrado com sucesso! Agora faça login.')

    user = User.objects.create_user(
        username=usuario, email=email, password=senha, first_name=nome, last_name=sobrenome)
    user.save()

    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form_contato = ContatoForm(user=request.user)
        form_categoria = CategoriaForm

        return render(request, 'accounts/dashboard.html', {'form_contato': form_contato, 'form_categoria': form_categoria})


@login_required(redirect_field_name='login')
def create_contact(request):
    if request.method == 'POST':
        form_contato = ContatoForm(
            request.POST, request.FILES, user=request.user)
        if "contato" in request.POST and form_contato.is_valid():
            contact = form_contato.save(commit=False)
            contact.created_by = contact.user = request.user

            form_contato.save()

            messages.success(request, 'Contato criado com sucesso!')
            return redirect('dashboard')

        else:
            messages.error(
                request, 'Erro ao enviar o formulário. Verifique se tudo está preenchido corretamente.')
            form = ContatoForm(request.POST)

            return render(request, 'accounts/dashboard.html', {'form_contato': form})


@login_required(redirect_field_name='login')
def create_category(request):
    if request.method == 'POST':
        form_categoria = CategoriaForm
        form_categoria = CategoriaForm(
            request.POST, initial={'created_by': request.user})

        if "categoria" in request.POST and form_categoria.is_valid():
            category = form_categoria.save(commit=False)
            category.created_by = request.user

            form_categoria.save()
            messages.success(request, 'Categoria criada com sucesso!')
            return redirect('dashboard')
        else:
            messages.error(
                request, 'Erro ao enviar o formulário. Verifique se tudo está preenchido corretamente.')
            form = CategoriaForm(request.POST)

            return render(request, 'accounts/dashboard.html', {'form_categoria': form})
