import json

def carregar_perguntas(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as f:
        perguntas = json.load(f)
    return perguntas