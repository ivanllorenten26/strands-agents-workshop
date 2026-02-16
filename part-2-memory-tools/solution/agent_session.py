"""
Session management in Strands Agents provides a robust mechanism
for persisting agent state and conversation history across multiple interactions.
This enables agents to maintain context and continuity even when the application restarts
or when deployed in distributed environments.

Strands offers two built-in session managers for persisting agent sessions:
- FileSessionManager: Stores sessions in the local filesystem
- S3SessionManager: Stores sessions in Amazon S3 buckets

https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/session-management/
"""

import os
import sys

from strands import Agent
from strands.session import FileSessionManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from terminal_loop import terminal_loop


def initialize_agent():
    # Create session manager.
    session_manager = FileSessionManager(session_id="current_user_session_id", storage_dir="./agent-session")

    # Use the following session manager with random UUID to see what happens every time you run the agent.
    # session_manager = FileSessionManager(session_id=uuid.uuid4(), storage_dir="./agent-session")

    # Create and configure the agent with the BedrockModel
    return Agent(
        # model= we're using the model by default.
        session_manager=session_manager,
        system_prompt="You are a helpful AI assistant participating in a Strands Agents workshop. "
                      "You help users understand agent concepts and answer their questions clearly."
                      "You also have memory.",
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
        print("Agent ready!\n")
        print("Tell your name, restart the agent and ask your name!\n")

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
