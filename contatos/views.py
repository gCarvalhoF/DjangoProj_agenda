from django.contrib.messages.api import add_message
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator
from contatos.models import Contato
from accounts.models import ContatoForm
from django.db.models import Q, Value
from django.contrib import messages
from django.db.models.functions import Concat
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(redirect_field_name='login')
def index(request):
    contatos = Contato.objects.order_by('-id').filter(
        mostrar=True,
        created_by=request.user
    )
    paginator = Paginator(contatos, 5)

    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/index.html', {
        'contatos': contatos,
    })


@login_required(redirect_field_name='login')
def details(request, contato_id):
    contato = get_object_or_404(
        Contato, id=contato_id, created_by=request.user)

    if not contato.mostrar:
        raise Http404

    return render(request, 'contatos/detalhes.html', {
        'contato': contato,
    })


def search(request):
    termo = request.GET.get('termo')
    campos = Concat('nome', Value(' '), 'sobrenome')
    if not termo:
        messages.add_message(
            request,
            messages.ERROR,
            'Campo de pesquisa não pode estar vazio.'
        )
        return redirect('index')

    contatos = Contato.objects.filter(created_by=request.user).annotate(
        nome_completo=campos
    ).filter(
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo),
        mostrar=True
    )

    paginator = Paginator(contatos, 5)

    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/index.html', {
        'contatos': contatos,
    })


@login_required(redirect_field_name='login')
def edit_contact(request, contact_id=0):
    if request.method != 'POST':
        contato = Contato.objects.get(id=contact_id)
        initial = {
            'id': contact_id,
            'nome': contato.nome,
            'sobrenome': contato.sobrenome,
            'telefone': contato.telefone,
            'email': contato.email,
            'data_criacao': contato.data_criacao,
            'descricao': contato.descricao,
            'created_by': contato.created_by,
            'categoria': contato.categoria,
            'mostrar': contato.mostrar,
            'foto': contato.foto,
        }
        form = ContatoForm(initial=initial, user=request.user)

        return render(request, 'contatos/detalhes.html', {'form': form, 'contato': contato})

    contato = Contato.objects.get(id=contact_id)

    mostrar = True if request.POST.get('mostrar') == 'on' else False

    contato.nome = request.POST.get(
        'nome') if request.POST.get('nome') else contato.nome
    contato.sobrenome = request.POST.get('sobrenome') if request.POST.get(
        'sobrenome') else contato.sobrenome
    contato.telefone = request.POST.get('telefone') if request.POST.get(
        'telefone') else contato.telefone
    contato.email = request.POST.get(
        'email') if request.POST.get('email') else contato.email
    contato.descricao = request.POST.get('descricao') if request.POST.get(
        'descricao') else contato.descricao
    contato.categoria = request.POST.get('categoria') if request.POST.get(
        'categoria') else contato.categoria
    contato.data_criacao = request.POST.get('data_criacao') if request.POST.get(
        'data_criacao') else contato.data_criacao
    contato.created_by = request.POST.get('created_by') if request.POST.get(
        'created_by') else contato.created_by
    contato.mostrar = mostrar
    contato.foto = request.FILES['foto'] if request.FILES else contato.foto

    contato.save()
    messages.success(request, 'Contato atualizado com sucesso!')
    return redirect('detalhes', contato_id=contact_id)
