# GameMind AI - CartPole visual

Esta versão adiciona um jogo real de demonstração com janela gráfica. A IA recebe quatro observações numéricas do ambiente (posição e velocidade do carrinho, ângulo e velocidade do poste), escolhe esquerda/direita e aprende com a pontuação recebida usando Q-Learning.

## Windows

Dê dois cliques em `INICIAR_CARTPOLE.bat`. Ou abra o CMD nesta pasta e execute:

```bat
py -m pip install -r requirements-cartpole.txt
py cartpole_train.py --episodes 8000
py cartpole_play.py
```

A memória persistente fica em `memory/cartpole_q.json`. Novos treinos continuam a partir dela.

## Importante

Este é um jogo de teste funcional para validar o ciclo de observação, decisão, recompensa e memória. A IA controla o CartPole, não Roblox ou Minecraft. Para conectar outro jogo é necessário criar um adaptador específico que traduza o estado desse jogo em observações, ações e recompensas. Esta versão usa os dados de estado fornecidos pelo ambiente, não visão computacional da tela.
