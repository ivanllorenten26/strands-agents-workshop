import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from strands import Agent
from strands.multiagent import GraphBuilder

from shared.terminal_loop import terminal_loop


def initialize_agent():
    researcher = Agent(name="researcher", system_prompt="You research...")
    analyst = Agent(name="analyst", system_prompt="You analyze...")
    fact_checker = Agent(name="fact_checker", system_prompt="You verify claims...")
    writer = Agent(name="writer", system_prompt="You write a report...")

    builder = GraphBuilder()

    builder.add_node(researcher, "research")
    builder.add_node(analyst, "analysis")
    builder.add_node(fact_checker, "fact_check")
    builder.add_node(writer, "report")

    builder.add_edge("research", "analysis")
    builder.add_edge("research", "fact_check")
    builder.add_edge("analysis", "report")
    builder.add_edge("fact_check", "report")

    builder.set_entry_point("research")
    builder.set_execution_timeout(600)  # seconds

    return builder.build()


def main():
    """
    Main entry point for the agent application.
    """
    print("=" * 60)
    print("Strands Agents Workshop - Part 4: Patterns - Graph")
    print("=" * 60)
    print()

    try:
        # Initialize the agent
        print("Initializing agent...")
        agent = initialize_agent()
        print("Agent ready! Try to ask \"Research the impact of AI on healthcare and create a report\"\n")

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
