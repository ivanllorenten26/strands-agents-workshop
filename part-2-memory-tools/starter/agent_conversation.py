"""
Conversation Manager

The SDK provides a flexible system for context management through the ConversationManager interface. This allows you to implement different strategies for managing conversation history. You can either leverage one of Strands's provided managers:

- NullConversationManager: A simple implementation that does not modify conversation history
- SlidingWindowConversationManager: Maintains a fixed number of recent messages (default manager)
- SummarizingConversationManager: Intelligently summarizes older messages to preserve context

https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/conversation-management/
"""
import os
import sys

from strands import Agent
from strands.agent import SlidingWindowConversationManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from terminal_loop import terminal_loop


def initialize_agent():
    # Let's create the Conversation Manager. Have a look at the docs.


    # Create and configure the agent with the BedrockModel
    return Agent(
        # model= we're using the model by default.
        conversation_manager=conversation_manager,
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
        print("Agent ready!\n")
        print("Tell your name, write 1 more question and then ask your name.\n")

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
