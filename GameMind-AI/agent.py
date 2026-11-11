import json
import random
from pathlib import Path

ACTIONS = ("up", "down", "left", "right")
DELTAS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
WIDTH, HEIGHT = 7, 6
START, GOAL = (0, 0), (6, 5)
WALLS = {(1, 0), (1, 1), (1, 3), (3, 1), (3, 2), (5, 2), (5, 3), (2, 4)}
MEMORY_PATH = Path("memory/q_table.json")


class Maze:
    def reset(self):
        self.position = START
        self.steps = 0
        return self.state()

    def state(self):
        return f"{self.position[0]},{self.position[1]}"

    def step(self, action):
        dx, dy = DELTAS[action]
        target = (self.position[0] + dx, self.position[1] + dy)
        self.steps += 1
        if not (0 <= target[0] < WIDTH and 0 <= target[1] < HEIGHT) or target in WALLS:
            reward = -5
        else:
            self.position = target
            reward = 50 if target == GOAL else -1
        return self.state(), reward, self.position == GOAL or self.steps >= 100

    def draw(self):
        for y in range(HEIGHT):
            print(" ".join(
                "A" if (x, y) == self.position else
                "G" if (x, y) == GOAL else
                "#" if (x, y) in WALLS else "."
                for x in range(WIDTH)
            ))
        print()


class QAgent:
    def __init__(self, alpha=0.15, gamma=0.95, epsilon=1.0):
        self.alpha, self.gamma, self.epsilon = alpha, gamma, epsilon
        self.q = {}
        self.games = 0
        self.wins = 0
        self.best_steps = None

    def values(self, state):
        return self.q.setdefault(state, {a: 0.0 for a in ACTIONS})

    def act(self, state, explore=True):
        if explore and random.random() < self.epsilon:
            return random.choice(ACTIONS)
        values = self.values(state)
        best = max(values.values())
        return random.choice([a for a, value in values.items() if value == best])

    def learn(self, state, action, reward, next_state, done):
        old = self.values(state)[action]
        future = 0.0 if done else max(self.values(next_state).values())
        self.values(state)[action] = old + self.alpha * (
            reward + self.gamma * future - old
        )

    def load(self):
        if not MEMORY_PATH.exists():
            return False
        data = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
        self.q = data.get("q", {})
        self.games = data.get("games", 0)
        self.wins = data.get("wins", 0)
        self.best_steps = data.get("best_steps")
        self.epsilon = data.get("epsilon", 0.2)
        return True

    def save(self):
        MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
        data = {"q": self.q, "games": self.games, "wins": self.wins,
                "best_steps": self.best_steps, "epsilon": self.epsilon}
        temporary = MEMORY_PATH.with_suffix(".tmp")
        temporary.write_text(json.dumps(data, indent=2), encoding="utf-8")
        temporary.replace(MEMORY_PATH)
