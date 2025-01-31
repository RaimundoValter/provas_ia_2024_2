from Utils import corrigir

# AP1-N2: Questões, rubricas e pontuação máxima
ap1_n2_questoes = ['1a) Uma empresa está desenvolvendo um sistema para classificar mensagens recebidas como "Urgente" ou "Não Urgente" com base nas palavras presentes na mensagem. Foi analisado um conjunto de 100 mensagens, e os dados a seguir foram coletados: Mensagens Urgentes: 30; Mensagens Não Urgentes: 70; Palavra Presente "imediatamente": 15 (Mensagens Urgentes) e  5 (Mensagens Não Urgentes); Palavra Presente "problema": 10 (Mensagens Urgentes) e 10 (Mensagens Não Urgentes); Palavra Presente "atraso": 8 (Mensagens Urgentes) e 12 (Mensagens Não Urgentes). Calcule as probabilidades de uma mensagem ser "Urgente" e "Não Urgente" com base no conjunto de dados fornecido. Adicionalmente, determine as probabilidades condicionais para cada palavra ("imediatamente", "problema" e "atraso") em relação às mensagens "Urgentes" e "Não Urgentes".',
                   '1b) Uma empresa está desenvolvendo um sistema para classificar mensagens recebidas como "Urgente" ou "Não Urgente" com base nas palavras presentes na mensagem. Foi analisado um conjunto de 100 mensagens, e os dados a seguir foram coletados: Mensagens Urgentes: 30; Mensagens Não Urgentes: 70; Palavra Presente "imediatamente": 15 (Mensagens Urgentes) e  5 (Mensagens Não Urgentes); Palavra Presente "problema": 10 (Mensagens Urgentes) e 10 (Mensagens Não Urgentes); Palavra Presente "atraso": 8 (Mensagens Urgentes) e 12 (Mensagens Não Urgentes). Suponha que uma nova mensagem contenha as palavras "imediatamente" e "problema". Calcule a probabilidade de ser uma mensagem "Urgente" e de ser "Não Urgente" utilizando o teorema de Bayes e classifique a mensagem como “Urgente” ou “Não Urgente”.',
                   '2a) Árvores de decisão são modelos amplamente utilizados para classificação e regressão. Explique como o conceito de ganho de informação é utilizado na construção de uma árvore de decisão. Detalhe mostrando o uso do cálculo de entropia e ganho de informação em um problema hipotético.',
                   '2b) Árvores de decisão são modelos amplamente utilizados para classificação e regressão. Suponha que você está desenvolvendo um sistema de suporte à decisão, aponte dois critérios de parada você utilizaria na construção da árvore de decisão para garantir um modelo eficiente?']

ap1_n2_rubricas=[
    {('Acertar a resposta aproximada de P("urgente")=30/100=0.30', 0.32),
     ('Acertar a resposta aproximada de P("não urgente")=70/100=0.70', 0.32),
     ('Acertar a resposta aproximada de P("imediatamente"|"urgente")=15/30=0.5', 0.32),
      ('Acertar a resposta aproximada de P("problema"|"urgente")=10/30~0.33', 0.32),
      ('Acertar a resposta aproximada de P("atraso"|"urgente")=8/30~0.27', 0.32),
       ('Acertar a resposta aproximada de P("imediatamente"|"não urgente")=5/70~0.07', 0.32),
        ('Acertar a resposta aproximada de P("problema"|"não urgente")=10/70~0.14', 0.32),
         ('Acertar a resposta aproximada de P("atraso"|"não urgente")=12/70~0.17', 0.32)},
       {('Calcular a probabilidade P("Urgente"|"imediatamente"&"problema")=(P("urgente")*P("imediatamente"|"urgente")*P("problema"|"urgente"))/(P("problema")*P("imediatamnte")), podendo simplificar para P("Urgente"|"imediatamente"&"problema")=P("urgente")*P("imediatamente"|"urgente")*P("problema"|"urgente") ~ 0.30 * 0.5 * 0.33 ~ 0.05', 1.0),
        ('Calcular a probabilidade P("Não Urgente"|"imediatamente"&"problema")=(P("Não urgente")*P("imediatamente"|"Não urgente")*P("problema"|"Não urgente"))/(P("problema")*P("imediatamnte")), podendo simplificar para P("Não Urgente"|"imediatamente"&"problema")=P("Não urgente")*P("imediatamente"|"Não urgente")*P("problema"|"Não urgente") ~ 0.70 * 0.07 * 0.014 ~ 0.001', 1.0),
         ('Classificar o e-mail como "URGENTE" baseado no cálculo do máximo argumento entre P("Urgente"|"imediatamente"&"problema") e P("Não Urgente"|"imediatamente"&"problema")', 0.5)},
          {('Demonstrar o cáculo de entropia inicial como sendo H("antes da partição")=-p("classe1")*log2(P("classe1"))-...-p("classeN")*log2(P("classeN"))', 1.0),
           ('Demonstrar o cáculo de entropia final como sendo H("depois da partição")=P("amostras irem para conjunto 1")*H("conjunto 1 após partição")+P("amostras irem para conjunto 2")*H("conjunto 2 após partição")', 1.0),
            ('Explicar que o conceito de Information Gain (IG) como sendo IG=H("antes da partição")-H("depois da partição") é essencial para decidir qual atributo/partição escolher a cada nível da árvore', 1.0)},
             {('Mencionar e/ou explicar dois ou mais critérios de parada válidos na construção de árvores de decisão.', 2.50),
              ('Mencionar e/ou explicar dois apenas um critério de parada válido na construção de árvores de decisão.', 1.25),
              ('Não mencionar e/ou explicar qualquer critério de parada na construção de árvores de decisão.',0.0)}]

ap1_n2_pontuacao_maxima = [2.5, 2.5, 2.5, 2.5]

ap1_n2 = [ap1_n2_questoes, ap1_n2_rubricas, ap1_n2_pontuacao_maxima]

corrigir('/content/provas_ia/N2-AP1', ap1_n2, alunos=['LUÃ MOREIRA PONCIANO',])