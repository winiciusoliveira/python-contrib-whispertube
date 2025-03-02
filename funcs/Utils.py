# Utils.py

import re

def formatar_nome(nome):
    """Formata o nome do arquivo removendo caracteres inválidos e substituindo espaços por '_'"""
    nome = re.sub(r'[^\w\s]', '', nome)  # Remove caracteres especiais
    nome = nome.replace(" ", "_")  # Substitui espaços por _
    return nome