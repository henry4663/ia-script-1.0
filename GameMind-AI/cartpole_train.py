import argparse
import random
import gymnasium as gym
from cartpole_agent import QAgent

def train(total_episodes):
    env = gym.make("CartPole-v1")
    agent = QAgent()
    resumed = agent.load()
    print("Memoria anterior carregada." if resumed else "Começando uma memória nova.")
    epsilon = 1.0
    epsilon_min = 0.05
    epsilon_decay = 0.9995

    try:
        for episode in range(1, total_episodes + 1):
            observation, _ = env.reset()
            state = agent.state(observation)
            score = 0
            while True:
                action = agent.act(state, epsilon)
                next_observation, reward, terminated, truncated, _ = env.step(action)
                next_state = agent.state(next_observation)
                done = terminated or truncated
                agent.learn(state, action, reward, next_state, done)
                state = next_state
                score += reward
                if done:
                    break

            agent.episodes += 1
            agent.best_score = max(agent.best_score, int(score))
            epsilon = max(epsilon_min, epsilon * epsilon_decay)

            if episode % 100 == 0:
                agent.save()
                print(
                    f"Episódio {episode}/{total_episodes} | "
                    f"pontuação: {int(score)} | recorde: {agent.best_score} | "
                    f"exploração: {epsilon:.3f}"
                )
    finally:
        agent.save()
        env.close()

    print("Treino finalizado. Memória salva em memory/cartpole_q.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=8000)
    args = parser.parse_args()
    train(max(1, args.episodes))
