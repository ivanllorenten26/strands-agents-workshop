"""
Strands Agents Workshop - Part 1: Introduction to Agents
Basic agent implementation with terminal UI loop

Your task: Complete the initialize_agent() function to create a working Strands agent.
The terminal loop is already implemented for you.
"""

import os
from dotenv import load_dotenv

# TODO: Add your imports here
# from strands import Agent
# from strands.models import BedrockModel

# Load environment variables
load_dotenv()


def initialize_agent():
    """
    Initialize and configure your Strands agent with AWS Bedrock.

    TODO: Import BedrockModel from strands.models and Agent from strands
    TODO: Create a BedrockModel instance with model_id and region_name
    TODO: Create an Agent with the BedrockModel
    TODO: Return the configured agent instance
    """
    # Your code here
    pass


def terminal_loop(agent):
    """
    Run an interactive terminal loop for the agent.
    This function is already implemented for you.
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
            response = agent(user_input)

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
    try:
        # Initialize the agent
        agent = initialize_agent()

        # Start the terminal loop
        terminal_loop(agent)

    except KeyboardInterrupt:
        print("\n\nExiting gracefully...")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        print("Goodbye!")


if __name__ == "__main__":
    main()
