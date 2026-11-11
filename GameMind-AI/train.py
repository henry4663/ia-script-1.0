import argparse
from agent import Maze, QAgent, GOAL, MEMORY_PATH


def train(episodes):
    env, agent = Maze(), QAgent()
    resumed = agent.load()
    print("Memória anterior carregada." if resumed else "Começando do zero.")
    wins_before = agent.wins

    for episode in range(1, episodes + 1):
        state = env.reset()
        while True:
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            agent.learn(state, action, reward, next_state, done)
            state = next_state
            if done:
                break

        agent.games += 1
        if env.position == GOAL:
            agent.wins += 1
            if agent.best_steps is None or env.steps < agent.best_steps:
                agent.best_steps = env.steps

        agent.epsilon = max(0.03, agent.epsilon * 0.997)
        if episode % 250 == 0:
            agent.save()
            print(f"Partida {episode}/{episodes} | vitórias: {agent.wins} | "
                  f"epsilon: {agent.epsilon:.3f} | melhor caminho: {agent.best_steps}")

    agent.save()
    print("\nTreino concluído!")
    print(f"Partidas totais: {agent.games}")
    print(f"Vitórias nesta sessão: {agent.wins - wins_before}")
    print(f"Melhor caminho: {agent.best_steps} passos")
    print(f"Memória salva em: {MEMORY_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Treinar a GameMind AI")
    parser.add_argument("--episodes", type=int, default=3000)
    args = parser.parse_args()
    train(max(1, args.episodes))
