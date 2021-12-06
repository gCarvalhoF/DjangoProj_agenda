from django.db import models
from contatos.models import Categoria, Contato
from django import forms


class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        exclude = ('created_by',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ContatoForm, self).__init__(*args, **kwargs)

        category_choices = list(Categoria.objects.filter(
            created_by=self.user))

        self.fields['categoria'] = forms.ChoiceField(
            choices=[(c.id, c.nome) for c in category_choices])


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        exclude = ('created_by',)
