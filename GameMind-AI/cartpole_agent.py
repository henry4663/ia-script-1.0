import json
from pathlib import Path
import numpy as np

MEMORY_PATH = Path("memory/cartpole_q.json")
ACTIONS = (0, 1)  # 0 = esquerda, 1 = direita

# Discretização das quatro medidas que o CartPole fornece.
BINS = (
    np.linspace(-2.4, 2.4, 7),
    np.linspace(-3.0, 3.0, 7),
    np.linspace(-0.2095, 0.2095, 11),
    np.linspace(-3.5, 3.5, 11),
)

class QAgent:
    def __init__(self, alpha=0.12, gamma=0.99):
        self.alpha = alpha
        self.gamma = gamma
        self.q = {}
        self.episodes = 0
        self.best_score = 0

    @staticmethod
    def state(observation):
        return tuple(
            int(np.digitize(float(value), edges))
            for value, edges in zip(observation, BINS)
        )

    def values(self, state):
        key = ",".join(map(str, state))
        if key not in self.q:
            self.q[key] = [0.0, 0.0]
        return self.q[key]

    def act(self, state, epsilon=0.0):
        import random
        if random.random() < epsilon:
            return random.choice(ACTIONS)
        values = self.values(state)
        if values[0] == values[1]:
            return random.choice(ACTIONS)
        return int(values[1] > values[0])

    def learn(self, state, action, reward, next_state, done):
        current = self.values(state)
        future = 0.0 if done else max(self.values(next_state))
        current[action] += self.alpha * (
            reward + self.gamma * future - current[action]
        )

    def load(self):
        if not MEMORY_PATH.exists():
            return False
        data = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
        self.q = data.get("q", {})
        self.episodes = int(data.get("episodes", 0))
        self.best_score = int(data.get("best_score", 0))
        return True

    def save(self):
        MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "q": self.q,
            "episodes": self.episodes,
            "best_score": self.best_score,
        }
        temp = MEMORY_PATH.with_suffix(".tmp")
        temp.write_text(json.dumps(data), encoding="utf-8")
        temp.replace(MEMORY_PATH)
