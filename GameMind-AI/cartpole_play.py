import time
import gymnasium as gym
from cartpole_agent import QAgent

def main():
    agent = QAgent()
    if not agent.load():
        print("Ainda não existe memória. Execute cartpole_train.py primeiro.")
        raise SystemExit(1)

    env = gym.make("CartPole-v1", render_mode="human")
    observation, _ = env.reset()
    state = agent.state(observation)
    score = 0
    print("GameMind está controlando o CartPole. Feche a janela para encerrar.")

    try:
        while True:
            action = agent.act(state, epsilon=0.0)
            observation, reward, terminated, truncated, _ = env.step(action)
            state = agent.state(observation)
            score += reward
            if terminated or truncated:
                print(f"Partida encerrada | pontuação: {int(score)}")
                time.sleep(1)
                observation, _ = env.reset()
                state = agent.state(observation)
                score = 0
    except KeyboardInterrupt:
        print("\nExecução encerrada.")
    finally:
        env.close()

if __name__ == "__main__":
    main()
