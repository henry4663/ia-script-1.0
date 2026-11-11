from agent import Maze, QAgent, GOAL

env, agent = Maze(), QAgent()
if not agent.load():
    print("Sem memória ainda. Execute primeiro: py train.py")
    raise SystemExit(1)

state = env.reset()
print(f"GameMind AI | partidas: {agent.games} | vitórias: {agent.wins}")
env.draw()
for turn in range(100):
    action = agent.act(state, explore=False)
    state, reward, done = env.step(action)
    print(f"Jogada {turn + 1}: {action} | recompensa: {reward}")
    env.draw()
    if done:
        print("A IA chegou ao objetivo!" if env.position == GOAL else
              "A partida terminou sem chegar ao objetivo.")
        break
