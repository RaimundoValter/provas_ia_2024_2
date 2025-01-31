# Teste unitário: escolhe_melhor()
from Utils import escolhe_melhor

teantativa_correcao_teste = [
        [
            {1: 'aqui é a avlaiação...', 2: 'este é o feedback...', 3: 2.0},
            {'clareza': 8.5, 'completude': 8.0, 'corretude': 9.0, 'precisão': 7.5}
        ],
        [
            {1: 'aqui é a avlaiação...', 2: 'este é o feedback...', 3: 1.55555},
            {'clareza': 6.0, 'completude': 6.5, 'corretude': 6.0, 'precisão': 7.0}
        ],
        [
            {1: 'aqui é a avlaiação...', 2: 'este é o feedback...', 3: 2.35},
            {'clareza': 9.0, 'completude': 9.5, 'corretude': 8.5, 'precisão': 8.0}
        ],
        [
            {1: 'aqui é a avlaiação...', 2: 'este é o feedback...', 3: 2.55555},
            {'clareza': 3.0, 'completude': 2.5, 'corretude': 3.5, 'precisão': 3.0}
        ]
    ]

try:
  nota_final, correcao_final = escolhe_melhor(teantativa_correcao_teste)
  print(f"Nota final: {nota_final:.2f}")
  print(f"Correção final: {correcao_final}")
except ValueError as e:
  print(f"Erro: {e}")