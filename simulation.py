import json
from typing import Dict, List

from agents import Agent
from environment import Environment


class Simulation:
    def __init__(self, environment: Environment, num_agents: int, steps: int) -> None:
        self.env = environment
        self.agents: List[Agent] = [Agent(agent_id=i, env=self.env) for i in range(num_agents)]
        self.steps = steps
        self.event_log: List[str] = []
        self.snapshots: List[Dict] = []

    def run(self) -> None:
        for step in range(self.steps):
            for agent in self.agents:
                agent.act(step, self.agents, self.event_log)

            # Environment dynamics
            self.env.regrow()

            # Periodic snapshot for visualization
            if step % 10 == 0 or step == self.steps - 1:
                self.snapshots.append(self._snapshot(step))

    def _snapshot(self, step: int) -> Dict:
        return {
            "step": step,
            "agents": [
                {"id": a.id, "x": a.x, "y": a.y, "energy": a.energy, "strategy": a.strategy}
                for a in self.agents
            ],
            # Downsample resources for lighter payload
            "resources": {
                "width": self.env.width,
                "height": self.env.height,
                "cells": self.env.resources,
            },
        }

    def save_results_json(self, output_path: str) -> None:
        data = {
            "meta": {"width": self.env.width, "height": self.env.height},
            "snapshots": self.snapshots,
            "log": self.event_log[-2000:],  # keep recent logs to limit size
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f)

