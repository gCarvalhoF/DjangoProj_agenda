# Generated by Django 3.2.9 on 2021-11-23 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contatos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contato',
            old_name='data_criacao',
            new_name='Data de criação',
        ),
    ]
