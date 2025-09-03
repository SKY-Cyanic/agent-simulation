import random
from typing import Dict, List, Tuple


class Agent:
    """
    Minimal agent capable of simple cooperate/compete actions on a grid.
    Agents move stochastically, harvest adjacent resources, and can trade.
    """

    def __init__(self, agent_id: int, env: "Environment") -> None:
        self.id = agent_id
        self.env = env
        self.energy: int = 100
        self.strategy: str = random.choice(["cooperate", "compete"])  # MVP strategies
        self.x: int
        self.y: int
        self.x, self.y = self.env.get_random_empty_cell()

    def act(self, step: int, agents: List["Agent"], event_log: List[str]) -> None:
        if self.energy <= 0:
            return

        # Movement: random walk with bounds
        dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)])
        self.x = max(0, min(self.env.width - 1, self.x + dx))
        self.y = max(0, min(self.env.height - 1, self.y + dy))
        self.energy -= 1

        # Harvest resource from the current cell
        harvested = self.env.harvest(self.x, self.y, amount=3)
        if harvested > 0:
            self.energy += harvested
            event_log.append(f"t={step} Agent_{self.id} harvested {harvested} @({self.x},{self.y})")

        # Interact with nearby agents
        neighbor = self._find_neighbor(agents)
        if neighbor is not None and neighbor.energy > 0:
            if self.strategy == "cooperate":
                self._cooperate(neighbor, step, event_log)
            else:
                self._compete(neighbor, step, event_log)

        # Occasional exploration strategy switch (very simple RL placeholder)
        if random.random() < 0.01:
            self.strategy = random.choice(["cooperate", "compete"])  # explore

    def _find_neighbor(self, agents: List["Agent"]) -> "Agent|None":
        candidates = [a for a in agents if a.id != self.id and abs(a.x - self.x) + abs(a.y - self.y) == 1]
        return random.choice(candidates) if candidates else None

    def _cooperate(self, other: "Agent", step: int, event_log: List[str]) -> None:
        # Share some energy if we have more than other
        if self.energy > other.energy + 5:
            transfer = min(5, self.energy // 10)
            if transfer > 0:
                self.energy -= transfer
                other.energy += transfer
                event_log.append(f"t={step} Agent_{self.id} cooperated -> Agent_{other.id} (+{transfer})")

    def _compete(self, other: "Agent", step: int, event_log: List[str]) -> None:
        # Attempt to steal energy with some probability; risk of backlash
        if random.random() < 0.4 and other.energy > 0:
            stolen = min(5, other.energy)
            other.energy -= stolen
            self.energy += stolen
            event_log.append(f"t={step} Agent_{self.id} stole {stolen} from Agent_{other.id}")
        elif random.random() < 0.1:
            # backlash cost
            cost = 2
            self.energy = max(0, self.energy - cost)
            event_log.append(f"t={step} Agent_{self.id} faced backlash (-{cost})")

