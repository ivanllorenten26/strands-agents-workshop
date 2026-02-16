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

    # TODO: Add nodes to the graph using builder.add_node(agent, "label")
    # Add all four agents: research, analysis, fact_check, report

    # TODO: Add edges to define the flow using builder.add_edge("from", "to")
    # The flow should be:
    #   research -> analysis
    #   research -> fact_check
    #   analysis -> report
    #   fact_check -> report

    # TODO: Set the entry point using builder.set_entry_point("label")

    # TODO: Set execution timeout using builder.set_execution_timeout(seconds)

    # TODO: Build and return the graph using builder.build()
    pass


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
