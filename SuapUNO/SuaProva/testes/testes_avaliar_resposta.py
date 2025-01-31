from Utils import avaliar_resposta

# Teste unitário: avaliar correção

questao_teste = "Explique o conceito de herança em orientação a objetos."

resposta_teste = "Herança é um mecanismo que permite que uma classe derive propriedades e comportamentos de outra classe."

rubricas_teste = {
    ('Explicação clara, mencionando os conceitos de classe base e classe derivada.', 2.5),
     ('Explicação correta, mas sem exemplos ou detalhes importantes.', 2.0),
      ('Explicação incompleta ou imprecisa, mas reconhecendo o conceito geral.', 1.0),
       ('Explicação incorreta ou ausente.', 0.0)
       }

pontuacao_maxima_teste = 2.5

dicionario_correcao_teste = {
    1: "A resposta está bem escrita, mas faltam exemplos concretos.",
    2: "Inclua exemplos de código para maior clareza.",
    3: 1.8
}

try:
    resultado = avaliar_resposta(questao_teste, resposta_teste, rubricas_teste, pontuacao_maxima_teste, dicionario_correcao_teste)
    print("Teste bem-sucedido! Resultado:", resultado)
except ValueError as e:
    print(f"Teste falhou com erro: {e}")