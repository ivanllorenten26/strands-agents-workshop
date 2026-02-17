"""
Tools Executors

https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/executors/
"""

import os
import sys

from strands import Agent, tool
from strands.tools.executors import ConcurrentToolExecutor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from terminal_loop import terminal_loop

def initialize_agent():
    # Create and configure the agent with the BedrockModel
    return Agent(
        # model= we're using the model by default.
        tool_executor=ConcurrentToolExecutor(),
        tools=[current_time, weather_in], # need to import or implement.
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
        print("Agent ready! Try to ask What is the time and the weather in Barcelona, Spain?\n")

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
