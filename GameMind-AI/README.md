# GameMind AI

IA local que aprende um labirinto por tentativa e erro usando Q-Learning.

## Recursos
- Aprendizado por reforço sem API, token ou serviço pago.
- Memória persistente em `memory/q_table.json`.
- Continua treinando a partir do conhecimento salvo.
- Exploração gradual e histórico de partidas.
- Demonstração da IA jogando no terminal do Windows.

## Requisitos
Python 3.10+; nenhuma biblioteca externa.

## CMD / PowerShell
Entre nesta pasta e execute:

```bat
py train.py --episodes 3000
py play.py
```

Para treinar mais: `py train.py --episodes 20000`.

Não apague `memory/q_table.json` se quiser preservar o aprendizado.

## Como funciona
O agente observa a posição, escolhe uma direção e recebe recompensas ou penalidades. O Q-Learning atualiza o valor esperado de cada ação. Esta versão aprende o labirinto demonstrativo; outros jogos precisam de um adaptador que forneça estado, ações e recompensas.
