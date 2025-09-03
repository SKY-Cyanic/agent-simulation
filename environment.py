import random
from typing import List, Tuple


class Environment:
    """
    Grid environment with renewable resources. Each cell has an integer resource
    amount that slowly regrows.
    """

    def __init__(self, width: int, height: int, resource_density: float) -> None:
        self.width = width
        self.height = height
        self.max_resource_per_cell = 10
        self.resources: List[List[int]] = self._generate_resources(resource_density)

    def _generate_resources(self, density: float) -> List[List[int]]:
        resources: List[List[int]] = []
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                if random.random() < density:
                    row.append(random.randint(3, self.max_resource_per_cell))
                else:
                    row.append(0)
            resources.append(row)
        return resources

    def get_random_empty_cell(self) -> Tuple[int, int]:
        return random.randrange(self.width), random.randrange(self.height)

    def harvest(self, x: int, y: int, amount: int) -> int:
        available = self.resources[y][x]
        taken = min(amount, available)
        self.resources[y][x] -= taken
        return taken

    def regrow(self) -> None:
        # Simple regrowth model: each cell has small chance to increase by 1
        for y in range(self.height):
            for x in range(self.width):
                if self.resources[y][x] < self.max_resource_per_cell and random.random() < 0.02:
                    self.resources[y][x] += 1

