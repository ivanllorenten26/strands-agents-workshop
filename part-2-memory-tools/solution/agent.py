"""
Strands Agents Workshop - Part 2: Memory and Tools
Complete solution with working agent implementation and terminal UI loop

This solution demonstrates:
1. How to initialize and configure a Strands agent
2. Handling user input through a terminal interface
3. Processing queries and generating responses
4. Maintaining a conversation loop with proper error handling

Note: AWS credentials are managed via Teleport. Make sure you have exported
the required environment variables before running this script.
"""

from strands import Agent, tool
from strands.models import BedrockModel
from strands.session import FileSessionManager
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from terminal_loop import terminal_loop


@tool
def calculate_sum(a: int, b: int) -> int:
    return a + b


def initialize_agent():
    """
    Initialize and configure a Strands agent with AWS Bedrock.

    Returns:
        Agent: Configured Strands agent instance using Bedrock Nova Lite
    """
    # Create a BedrockModel instance with the desired configuration
    bedrock_model = BedrockModel(
        model_id="eu.amazon.nova-lite-v1:0",
        region_name="eu-central-1",
    )

    # Create session manager.
    session_manager = FileSessionManager("current_user_session_id", storage_dir="./agent-session")

    # Create and configure the agent with the BedrockModel
    agent = Agent(
        model=bedrock_model,
        session_manager=session_manager,
        tools=[calculate_sum],
        system_prompt="You are a helpful AI assistant participating in a Strands Agents workshop. "
                      "You help users understand agent concepts and answer their questions clearly."
                      "You also have memory.",
    )

    return agent

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
        print("Agent ready!\n")

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
