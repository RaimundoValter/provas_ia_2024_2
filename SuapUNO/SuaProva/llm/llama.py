import math

def llama(prompt_llama, max_tentativas = 5):
  """
  Envia um prompt para um modelo de linguagem hospedado na API Groq e retorna a resposta gerada.

  A função tenta se conectar ao serviço da Groq para gerar uma resposta ao prompt fornecido.
  Em caso de erro de limitação de serviço (rate limit), aplica uma política de backoff exponencial
  para aguardar antes de realizar novas tentativas. Após exceder o número máximo de tentativas,
  uma exceção é levantada.

  Args:
      prompt_llama (str): O texto de entrada que será enviado para o modelo de linguagem.
      max_tentativas (int, opcional): O número máximo de tentativas permitidas antes de falhar.
          Valor padrão: 3.

  Returns:
      str: A resposta gerada pelo modelo de linguagem.

  Raises:
      Exception: Levantada se o número máximo de tentativas for excedido ou se ocorrer
          um erro inesperado que não seja de limitação de serviço.

  Exemplo:
      >>> resposta = llama("O que é inteligência artificial?")
      >>> print(resposta)
      "Inteligência artificial é um ramo da ciência da computação que se concentra na criação de sistemas..."
  """
  cliente = Groq(api_key = CHAVE_GROQ)
  tentativas = 0
  servico_limitado = False
  aguardar_em_segundos = 2 * 60

  while tentativas < max_tentativas:
    try:
      chat_completion = cliente.chat.completions.create(
          messages=[
              {
                  "role": "user",
                  "content": prompt_llama,
              }
          ],
          model=modelo_llama,
      )
      return chat_completion.choices[0].message.content
    except Exception as e:
      if "service limited" in str(e).lower() or "rate limit" in str(e).lower():

        if servico_limitado:
          aguardar_em_segundos += (2 * 60) # Caso o serviço já esteja limitado, amplia o tempo de aguardo.
        else:
          servico_limitado = True # Caso seja a primeira vez que o serviço foi limitado pela groq.com

        

        # Tenta recuperar o tempo para aguardar vindo da mensagem Groq:
        tempo_aguardar_groq = re.search(r"(\d+)m([\d.]+)s", str(e))
        
        if tempo_aguardar_groq:
          minutos = float(tempo_aguardar_groq.group(1))
          segundos = float(tempo_aguardar_groq.group(2))
          aguardar_em_segundos = int(math.ceil(minutos * 60 + segundos + 15))

        print(f"Tentativa {tentativas + 1} de {max_tentativas}...\nServiço limitado, aguardando {aguardar_em_segundos//60} minuto(s)...")
        time.sleep(aguardar_em_segundos)

        tentativas += 1
      else:
        print(f"Erro inesperado: {e}")
        tentativas += 1
        #raise e
  # Caso exceda o número de tentativas sem ter retorno.
  raise Exception("Falha após várias tentativas. Tente novamente mais tarde.")