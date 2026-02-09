"""
The AgentCore Memory Session Manager leverages Amazon Bedrock AgentCore Memory to provide
advanced memory capabilities with intelligent retrieval for Strands Agents.
It supports both short-term memory (STM) for conversation persistence and long-term memory (LTM)
with multiple strategies for learning user preferences, facts, and session summaries.

https://strandsagents.com/latest/documentation/docs/community/session-managers/agentcore-memory/
"""

import os
import sys
import uuid

from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager
from strands import Agent

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from terminal_loop import terminal_loop


def initialize_agent():
    # Have a look at the docs to create the session manager.

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
