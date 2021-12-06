from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator
from contatos.models import Contato
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
