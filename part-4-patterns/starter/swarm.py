import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from strands import Agent
from strands.multiagent import Swarm

from shared.terminal_loop import terminal_loop


def initialize_agent():
    researcher = Agent(name="researcher", system_prompt="You research and gather facts...")
    coder = Agent(name="coder", system_prompt="You write code...")
    reviewer = Agent(name="reviewer", system_prompt="You review and improve code...")
    architect = Agent(name="architect", system_prompt="You design the system...")

    # TODO: Create and return a Swarm with the agents above.
    # Hint: Use the Swarm class with:
    #   - A list of agents: [coder, researcher, reviewer, architect]
    #   - entry_point: the agent that starts (researcher)
    #   - max_handoffs: 20
    #   - max_iterations: 20
    #   - execution_timeout: 900.0
    #   - node_timeout: 300.0
    pass


def main():
    """
    Main entry point for the agent application.
    """
    print("=" * 60)
    print("Strands Agents Workshop - Part 4: Patterns - Swarm")
    print("=" * 60)
    print()

    try:
        # Initialize the agent
        print("Initializing agent...")
        agent = initialize_agent()
        print("Agent ready! Try to ask Design and implement a simple REST API for a todo app\n")

        # Start the terminal loop
        terminal_loop(agent)

    except KeyboardInterrupt:
        print("\n\nExiting gracefully...")
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure you have:")
        print("1. Created a .env file with your AWS credentials")
        print("2. Installed dependencies: pip install -r requirements.txt")
        print("3. AWS Bedrock access enabled in eu-central-1 region")
    finally:
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
