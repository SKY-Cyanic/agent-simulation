from simulation import Simulation
from environment import Environment


def main() -> None:
    """
    Entry point for running a local simulation. Outputs a JSON snapshot to
    docs/data/sim.json so the GitHub Pages frontend can visualize it.
    """
    environment = Environment(width=50, height=50, resource_density=0.2)
    simulation = Simulation(environment=environment, num_agents=100, steps=300)

    simulation.run()
    # Persist results into docs/ for GitHub Pages visualization
    simulation.save_results_json(output_path="docs/data/sim.json")


if __name__ == "__main__":
    main()

