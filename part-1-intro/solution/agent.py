"""
Strands Agents Workshop - Part 1: Introduction to Agents
Complete solution with working agent implementation and terminal UI loop

This solution demonstrates:
1. How to initialize and configure a Strands agent
2. Handling user input through a terminal interface
3. Processing queries and generating responses
4. Maintaining a conversation loop with proper error handling
"""

import os
from dotenv import load_dotenv
from strands import Agent
from strands.models import BedrockModel

# Load environment variables from .env file
load_dotenv()


def initialize_agent():
    """
    Initialize and configure a Strands agent with AWS Bedrock.

    Returns:
        Agent: Configured Strands agent instance using Bedrock Nova Lite
    """
    # Create a BedrockModel instance with the desired configuration
    bedrock_model = BedrockModel(
        model_id=os.getenv("MODEL", "eu.amazon.nova-lite-v1:0"),
        region_name="eu-central-1",
    )

    # Create and configure the agent with the BedrockModel
    agent = Agent(
        model=bedrock_model,
        system_prompt="You are a helpful AI assistant participating in a Strands Agents workshop. "
        "You help users understand agent concepts and answer their questions clearly.",
    )

    return agent


def terminal_loop(agent):
    """
    Run an interactive terminal loop for the agent.

    Args:
        agent: Initialized Strands agent instance
    """
    print("Agent initialized! Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()

            # Check for exit commands
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\nAgent: Goodbye! Thanks for chatting!")
                break

            # Skip empty inputs
            if not user_input:
                continue

            # Process the query with the agent
            response = agent.run(user_input)

            # Display the response
            print(f"\nAgent: {response}\n")

        except KeyboardInterrupt:
            print("\n\nInterrupted by user...")
            break
        except Exception as e:
            print(f"\nError processing request: {e}\n")
            continue


def main():
    """
    Main entry point for the agent application.
    """
    print("=" * 60)
    print("Strands Agents Workshop - Part 1: Basic Agent")
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
