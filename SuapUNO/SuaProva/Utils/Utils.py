import os
import re
import time
from groq import Groq
from PyPDF2 import PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import numpy as np
from scipy.stats import zscore
import os
import re
import ast
from pprint import pprint
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.units import inch

def recupera_avaliacoes(nome_pasta):
    """
    Processa arquivos de texto contendo avaliações de estudantes em uma pasta específica.

    Esta função realiza as seguintes etapas:
    1. Lista todos os arquivos com extensão .txt na pasta fornecida.
    2. Lê o conteúdo de cada arquivo e associa ao nome do estudante, extraído do nome do arquivo.
    3. Extrai as respostas dos estudantes no formato esperado, separando-as por questões indicadas pelos padrões como '1)', '2a)', '2b)', etc.

    Args:
        nome_pasta (str): Caminho para a pasta contendo os arquivos de texto das avaliações.

    Returns:
        list: Uma lista de listas, onde cada sublista contém:
              - O nome do estudante (str).
              - Uma lista de strings com as respostas extraídas de cada questão (list).

    Raises:
        FileNotFoundError: Se a pasta fornecida não for encontrada.
        ValueError: Se o formato esperado dos arquivos de texto não for atendido.
    """
    # Listar apenas arquivos com extensão .txt
    arquivos_txt = [f for f in os.listdir(nome_pasta) if f.endswith('.txt') and os.path.isfile(os.path.join(nome_pasta, f))]

    print("Arquivos .txt na pasta:")
    for arquivo in arquivos_txt:
        print(arquivo)
    print("\n\n")

    # Lista para armazenar o conteúdo de cada arquivo
    avaliacoes = []
    nomes_estudantes = []

    # Ler o conteúdo de cada arquivo e adicioná-lo à lista
    for arquivo in arquivos_txt:
        nomes_estudantes.append(arquivo.strip('.txt'))
        with open(os.path.join(nome_pasta, arquivo), 'r', encoding="ISO-8859-1") as f: #"ISO-8859-1"
            conteudo = f.read()
            avaliacoes.append(conteudo)

    # Separação das respostas
    respostas_estudantes = []
    for idx, avaliacao in enumerate(avaliacoes):
      # Regex para capturar questões no formato ##<<...>>## seguido pelo conteúdo da questão
      padrao = r"##<<(.+?)>>##(.*?)(?=##<<.+?>>##|$)"
      respostas = re.findall(padrao, avaliacao, re.DOTALL)
      respostas_formatadas = [f"{identificador}) {'<<QUESTÃO NÃO RESPONDIDA>>' if conteudo.strip()== '' else conteudo.strip()}" for identificador, conteudo in respostas]
      respostas_estudantes.append([nomes_estudantes[idx], respostas_formatadas])

    return respostas_estudantes


def extrair_dicionario(texto):
  """
  Extrai o primeiro dicionário Python válido de uma string usando expressão regular.

  A função reformata o dicionário:
  - Substitui as chaves originais por índices numéricos sequenciais.
  - Se o dicionário possui uma terceira chave, tenta converter seu valor para float.

  Args:
      texto (str): Texto contendo um ou mais dicionários.

  Returns:
      dict: O dicionário formatado com chaves numéricas, ou None se nenhum dicionário válido for encontrado.
  """
  # Expressão regular para capturar estruturas parecidas com dicionários
  padrao = r'\{.*?\}'

  # Buscar todas as ocorrências no texto
  correspondencias = re.findall(padrao, texto, re.DOTALL)

  for texto in correspondencias:
    try:
      # Tenta converter a string para um dicionário Python
      texto_limpo = re.sub(r'\\n+', r' ', texto)
      texto_limpo = re.sub(r'\s+', ' ', texto_limpo)
      texto_limpo = re.sub(r'`', "'", texto_limpo)
      dicionario = ast.literal_eval(texto_limpo)

      if isinstance(dicionario, dict):

        dicionario_formatado = dict()

        # Verificando se é um dicionário de chaves numéricas: representando um dicionário de correção.
        if all(map(lambda elemento: str(elemento).isnumeric(), dicionario.keys())) and len(dicionario) == 3:

          # Para garantir que as chaves sejam números
          for idx, valor in enumerate(dicionario.values(), start=1):
            if idx == 3:
              dicionario_formatado[idx] = float(valor)
            else:
              dicionario_formatado[idx] = str(valor)

          return dicionario_formatado

        elif all(map(lambda elemento: str(elemento).isalpha(), dicionario.keys())) and len(dicionario) == 4: # Verifica se é um dicionário de avaliação de correção.

          # Para garantir que as chaves sejam as strings esperadas.
          valores_dicionario = list(dicionario.values())

          for idx, chave in enumerate(['clareza', 'completude', 'corretude', 'precisao']):
            dicionario_formatado[chave] = int(valores_dicionario[idx])

          return dicionario_formatado

      # Caso não seja um dicionário.
      continue

    except (SyntaxError, ValueError):

      print(f"\nErro ao converte dicionário, tentanto novamente...")
      # Ignora strings que não sejam dicionários válidos
      continue

  # Retorna None se nenhum dicionário válido for encontrado
  return None

# Avaliar resposta
def avaliar_resposta(questao, resposta, rubricas, pontuacao_maxima, dicionario_correcao):
  """
  Avalia a correção de uma pergunta respondida por um estudante, atribuindo pontuações
  com base em clareza, completude, corretude e precisão.

  Args:
      questao (str): A pergunta avaliada.
      resposta (str): A resposta fornecida pelo estudante.
      rubricas (str, float): Rubircas de avaliação detalhadas com pontuações específicas.
      pontuacao_maxima (float): Pontuação máxima atribuível para a resposta.
      dicionario_correcao (dict): Contém:
          - 1: Texto da correção.
          - 2: Feedback adicional.
          - 3: Pontuação atribuída pela correção.

  Returns:
      dict: Um dicionário contendo as pontuações para os critérios:
          - 'clareza': float (0.0 a 10.0)
          - 'completude': float (0.0 a 10.0)
          - 'corretude': float (0.0 a 10.0)
          - 'precisão': float (0.0 a 10.0)

  Raises:
      ValueError: Se nenhuma resposta válida for gerada após múltiplas tentativas.
  """
  prompt = f"""
  Esqueça o que foi dito antes.
  Considere os seguintes dados:
  **Pergunta**: {questao}
  **Resposta do estudante**: {resposta}
  **Rubricas** (com pontuações): {rubricas}
  **Pontuação máxima**: {pontuacao_maxima}
  **Texto da correção**: {dicionario_correcao[1]}
  **Feedback da correção**: {dicionario_correcao[2]}
  **Pontuação da correção**: {dicionario_correcao[3]}
  **Tarefa**:
  Avalie a correção da pergunta com base nas rubricas fornecidas.
  Atribua pontuações de 0 a 10 para clareza, completude, corretude, precisão.

  **Formato da resposta**:
  Retorne a resposta estritamente em formato de dicionário python com as seguintes chaves e valores, sem alucinar:
  {{'clareza': 'pontuação no formato float entre 0.0 e 10.0', 'completude': 'pontuação no formato float entre 0.0 e 10.0', 'corretude': 'pontuação no formato float entre 0.0 e 10.0', 'precisão': 'pontuação no formato float entre 0.0 e 10.0'}}

  **Dicionário Python**:
  """
  # Inicializa tentativa
  tentativa = 0
  max_tentativas = 4
  dicionario_resultado = None

  while dicionario_resultado is None and tentativa < max_tentativas:
    resposta_ia = llama(prompt)
    #pprint(resposta_ia)
    #print("\n")
    dicionario_resultado = extrair_dicionario(resposta_ia)
    tentativa += 1
    print(f"\nAvaliando a correção, tentativa {tentativa} de {max_tentativas}...")

  if dicionario_resultado is None:
    raise ValueError("Não foi possível gerar uma avaliação válida após várias tentativas.")

  return dicionario_resultado

from scipy.stats import zscore

def escolhe_melhor(tentativas_correcao):
  """
  Seleciona a melhor tentativa de correção com base na qualidade e calcula uma nota final ponderada,
  removendo outliers para garantir resultados mais consistentes.

  Args:
      tentativas_correcao (list): Uma lista onde cada elemento é uma tentativa de correção no formato:
          [
              [correcao, ...],
              {'clareza': float, 'completude': float, 'corretude': float, 'precisão': float}
          ]

  Returns:
      tuple: Um par contendo:
          - nota_final (float): A nota final ponderada após a exclusão de outliers.
          - correcao_final (any): A melhor correção escolhida com base na mediana das qualidades.

  Raises:
      ValueError: Se a lista de tentativas estiver vazia ou se todas forem consideradas outliers.
  """
  if not tentativas_correcao:
    raise ValueError("A lista de tentativas de correção está vazia.")

  # Extrai notas e calcula qualidade total de cada correção
  notas = [float(correcao[0][3]) for correcao in tentativas_correcao]
  qualidades = [sum([float(valor) for valor in correcao[1].values()]) for correcao in tentativas_correcao]

  # Identificar e excluir outliers usando z-score
  z_scores = zscore(notas)
  outliers = [nota for nota, z in zip(notas, z_scores) if abs(z) > 2]

  for outlier in outliers:
    idx = notas.index(outlier)
    notas.pop(idx)
    qualidades.pop(idx)
    tentativas_correcao.pop(idx)

  if not notas:
    raise ValueError("Todas as tentativas foram consideradas outliers.")

  # Escolhe a melhor correção com base na mediana das qualidades
  lista_melhores = sorted(zip(qualidades, tentativas_correcao), key=lambda x: x[0])
  
  # Escolhe a correção de mais alta qualidade.
  correcao_final = lista_melhores[-1][1][0]

  # Seleciona a nota final da questão.
  nota_final = correcao_final[3] 

  return nota_final, correcao_final

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap
from datetime import datetime, timezone
import pytz

def montar_pdf_correcao(nome_estudante_, perguntas, rubricas, respostas_estudante, avaliacao_corrigida, nome_pasta="."):
    """
    Gera um arquivo PDF contendo a correção detalhada de uma avaliação.

    Args:
        nome_estudante_ (str): Nome do estudante.
        perguntas (list): Lista de perguntas realizadas na avaliação.
        rubricas (list): Lista de rubricas para as respostas esperadas.
        respostas_estudante (list): Lista de respostas fornecidas pelo estudante.
        avaliacao_corrigida (list): Lista de tuplas contendo:
            - Nota da questão (float).
            - Detalhes da correção (dict) com as chaves:
                - 'consideracoes': Considerações sobre a resposta do estudante.
                - 'feedback': Feedback fornecido.
                - 'pontuacao': Pontuação atribuída.
        nome_pasta (str, optional): Diretório onde o arquivo PDF será salvo.
                                    Padrão é o diretório atual (".").

    Returns:
        str: Caminho do arquivo PDF gerado.

    Raises:
        ValueError: Se o tamanho das listas de perguntas, rubricas ou respostas não coincidir.

    """
    # Validação das listas
    if not (len(perguntas) == len(rubricas) == len(respostas_estudante) == len(avaliacao_corrigida)):
        raise ValueError("As listas de perguntas, rubricas, respostas e avaliações devem ter o mesmo tamanho.")

    # Cálculo da pontuação total
    pontuacao_total = sum(nota for nota, _ in avaliacao_corrigida)

    print(f"Atribuído nota {pontuacao_total:.2f} para {nome_estudante_}...")
    
    fuso_sao_paulo = pytz.timezone("America/Sao_Paulo")
    hora_atual_sp = datetime.now(fuso_sao_paulo)

    data_hora = hora_atual_sp.strftime("%Y-%m-%d %Hh%Mm")
    # Nome do arquivo PDF
    nome_arquivo_pdf = f"{nome_pasta}/Correção do {nome_estudante_} - {data_hora} - Nota {pontuacao_total:.2f}.pdf"

    # Configuração do PDF
    c = canvas.Canvas(nome_arquivo_pdf, pagesize=letter)
    c.setFont("Helvetica-Bold", 10)
    largura, altura = letter
    margem = 50  # Margem do documento
    largura_texto = largura - 2 * margem
    linha_atual = altura - margem  # Posição inicial no topo da página
    espaco_entre_linhas = 12  # Espaço entre as linhas

    # Função para adicionar texto ao PDF com controle de quebras de linha
    def adicionar_texto(texto, c, linha_atual):
        linhas = wrap(texto, width=95)  # Ajuste o valor para controlar a largura do texto
        for linha in linhas:
            if linha_atual <= margem:
                c.showPage()  # Cria uma nova página se necessário
                linha_atual = altura - margem
            c.drawString(margem, linha_atual, linha)
            linha_atual -= espaco_entre_linhas
        return linha_atual

    # Texto do PDF
    correcao = f"Nome: {nome_estudante_}\n"
    correcao += f"Pontuação Total da Avaliação: {pontuacao_total:.2f} pontos\n"
    correcao += "=" * 25 + "\n"

    for id, pergunta in enumerate(perguntas):
        correcao += f"Correção da Questão {id+1}:\n"
        correcao += f"Pergunta: {pergunta}\n\n"
        correcao += "=" * 10 + "Rubrica(s)\n"
        
        for rubrica in rubricas[id]:
          correcao += f"{rubrica}\n"

        correcao += "=" * 10 + f"Resposta do estudante da questão {id+1}:\n"
        correcao += f"{respostas_estudante[id]}\n\n"
        correcao += "=" * 25 + "\n"
        correcao += f"Correção proposta pela IA:\n"
        correcao += "=" * 25 + "\n"
        correcao += "=" * 10 + f"Considerações:\n"
        correcao += f"{avaliacao_corrigida[id][1][1]}\n\n"
        correcao += "=" * 10 + "Feedback:\n"
        correcao += f"{avaliacao_corrigida[id][1][2]}\n\n"
        correcao += "=" * 10 + "Pontuação:\n"
        correcao += f"{avaliacao_corrigida[id][1][3]}\n\n"
        correcao += "=" * 25 + "\n"

    # Adicionar texto ao PDF
    for linha in correcao.split("\n"):
        linha_atual = adicionar_texto(linha, c, linha_atual)

    # Salvar o PDF
    c.save()
    print(f"Correção gravada em: {nome_arquivo_pdf}")
    return nome_arquivo_pdf


def corrigir(nome_pasta, gabarito_avaliacao, REPETIR_CORRECAO = 3, alunos = []):
  questoes = gabarito_avaliacao[0]
  rubricas = gabarito_avaliacao[1]
  pontuacao_maxima = gabarito_avaliacao[2]
  avaliacoes = recupera_avaliacoes(nome_pasta)


  avaliacoes_para_correcao = []

  if alunos != []:
    for avaliacao in avaliacoes:
      if avaliacao[0].strip('.txt') in alunos:
        avaliacoes_para_correcao.append(avaliacao)

  else:
    avaliacoes_para_correcao = avaliacoes

  # Para cada avaliação de um estudante
  for avaliacao in avaliacoes_para_correcao:

    # print("")
    # pprint(avaliacao)
    # print("")

    nome_arquivo = avaliacao[0].strip('.txt')
    #nome_estudante = avaliacao[0].split('- ')[0].strip('.txt')
    nome_estudante = nome_arquivo
    respostas = avaliacao[1]

    print(f"Avaliando o aluno {nome_estudante}...")

    avaliacao_corrigida = []

    # Para cada Questão em uma avaliação específica
    for numero_questao, questao in enumerate(questoes):

      if '<<QUESTÃO NÃO RESPONDIDA>>' in respostas[numero_questao]:
        print(f"Questão {numero_questao +1 } está vazia...")
        avaliacao_corrigida.append([0.0 , {1:"",2:"",3:0.0}])
        continue

      prompt = f"""
Esqueça o que foi dito antes.
Considere os seguintes dados:
**Pergunta**: {questao}
**Resposta do estudante**: {respostas[numero_questao]}
**Rubricas**: {rubricas[numero_questao]}
**Pontuação máxima**: {pontuacao_maxima[numero_questao]}
Assuma que o estudante possui um conhecimento **básico** sobre o assunto avaliado.
**Tarefa**:
- Corrija a resposta do estudante considerando as rubricas fornecidas.
- Seja flexível e atribua nota máxima na rubrica caso o estudante atinja parcialmente a descrição da rubrica.

**Formato da resposta**:
Retorne a resposta estritamente em formato de dicionário Python (chaves em formato de números inteiros e valores associados às chaves em formato string) com as seguintes chaves e valores, sem alucinar:
{{1: 'texto completo da avaliação da resposta do estudante em relação às rubircas fornecidas',
  2: 'texto com o feedback detalhado sobre os pontos fortes e as melhorias necessárias na resposta para atingir nota máxima na questão completa, caso não tenha atingido a nota máxima.',
  3: 'pontuação no formato float, garantindo que o total não ultrapasse a pontuação máxima e reflita a nota do item avaliado em acordo com as rubricas da questão avaliada.'}}

**Dicionário Python**:
"""

      qtd_correcoes = 0
      tentativas_correcao = []

      # Faz 5 tentativas para verificar qual correção foi a melhor.
      while qtd_correcoes < REPETIR_CORRECAO:
        print(f"\nCorrigindo a questão {numero_questao + 1}, vez {qtd_correcoes+1} de {REPETIR_CORRECAO}...")
        # Correção pela Llama
        resposta_ia = llama(prompt)

        # Extração do dicionário contendo a correção.
        dicionario_correcao = extrair_dicionario(resposta_ia)

        # Caso a resposta seja válida
        if dicionario_correcao is not None:
          # Avalia a qualidade da resposta solicitando ao Llama que avalie a própria
          qualidade_correcao = avaliar_resposta(questao, respostas[numero_questao], rubricas[numero_questao], pontuacao_maxima[numero_questao], dicionario_correcao)
          # Grava a correção e a avaliação da qualidade dessa correção
          tentativas_correcao.append([dicionario_correcao, qualidade_correcao])
          qtd_correcoes += 1

      #Ao terminar as 5 correções e suas avaliações, escolhe a melhor entre elas e grava a média das notas e a correção com melhor avaliação.
      avaliacao_corrigida.append(escolhe_melhor(tentativas_correcao))

      print(f"\nQuestão {numero_questao + 1}: ok!")
      
      if (numero_questao + 1) < len(questoes):
        print("\nIndo para próxima questão >>>")
      else:
        print(f"Finalizado a avaliação de {nome_estudante}!")

    #pprint(avaliacao_corrigida)

    # Ao finalizar uma correção completa, grava o resultado em pdf para aquele estudante.
    montar_pdf_correcao(nome_estudante, questoes, rubricas, respostas, avaliacao_corrigida, nome_pasta+"/correções")

    # pprint(avaliacao_corrigida)