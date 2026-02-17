import os
import sys

from strands import Agent

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from terminal_loop import terminal_loop
from strands_tools import calculator


def initialize_agent():
    return Agent(
        # model= we're using the model by default.
        # Here you need to specify tools. Try to use https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/community-tools-package/
        system_prompt="You are a helpful AI assistant participating in a Strands Agents workshop. "
                      "You help users understand agent concepts and answer their questions clearly.",
    )

def main():
    """
    Main entry point for the agent application.
    """
    print("=" * 60)
    print("Strands Agents Workshop - Part 2: Memory and Tools")
    print("=" * 60)
    print()

    try:
        # Initialize the agent
        print("Initializing agent...")
        agent = initialize_agent()
        print("Agent ready! Try to ask What is 42 ^ 9\n")

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
