import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from strands import Agent, tool

from shared.terminal_loop import terminal_loop


# TODO: Create a specialised agent that can be used as a tool.
# Hint: Use the @tool decorator on a function that returns an Agent instance.
# The agent should be an expert in Cards, in the context of a Bank.


def initialize_agent():
    orchestrator = Agent(
        # model= we're using the model by default.
        # TODO: Add the tools parameter to include your specialised agent tool
        # Hint: tools=[your_tool_function]
        system_prompt="Route queries to specialized agents:"
                      "- cards questions -> cards_specialised_agent",
    )
    return orchestrator


def main():
    """
    Main entry point for the agent application.
    """
    print("=" * 60)
    print("Strands Agents Workshop - Part 4: Patterns - Agents as Tools")
    print("=" * 60)
    print()

    try:
        # Initialize the agent
        print("Initializing agent...")
        agent = initialize_agent()
        print("Agent ready! Try to ask What is a debit card\n")

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
