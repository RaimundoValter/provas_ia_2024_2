from Utils import extrair_dicionario
from pprint import pprint

# Teste unitário: extrair_dicionario():

# Testando o dicionário de correção de avaliação.
texto_inesperado1 = """
Lorem ipsum { 'a': 'valor 1', 'b': 42, 'c': 'valor 3', 'd': 3.14 } dolor sit amet.
"""

texto_esperado1 = """
Lorem ipsum { 1 : 'aqui é a avlaiação...', '2': 'este é o feedback...', '3' : '2.55555',} dolor sit amet.
"""

print("Para o texto inesperado: ")
pprint(extrair_dicionario(texto_inesperado1))

print("Para o texto esperado: ")
pprint(extrair_dicionario(texto_esperado1))

print("\n\n")

# Testando a extração do dicionário de avaliação da correção.

texto_inesperado2 = """
Lorem ipsum { 1: 'clareza', 'completude': 4, 'corretude': '3', 'precisão': 3.14 } dolor sit amet.
"""

texto_esperado2 = """
Lorem ipsum { 'clareza' : 1, 'completude': 4, 'corretude': '3', 'precisão': 3.14} dolor sit amet.
"""

print("Para o texto inesperado: ")
pprint(extrair_dicionario(texto_inesperado2))

print("Para o texto esperado: ")
pprint(extrair_dicionario(texto_esperado2))