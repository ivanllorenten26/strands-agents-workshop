import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from strands import Agent, tool

from shared.terminal_loop import terminal_loop

import logging

logging.basicConfig(level=logging.INFO)

@tool
def debit_cards_specialised_agent():
    """Use this tool ONLY when the user's query is specifically about debit cards."""
    logging.info("Calling debit_cards_specialised_agent")
    agent = Agent(system_prompt="You are an expert in Debit Cards, in the context of a Bank.")
    return agent


@tool
def credit_cards_specialised_agent():
    """Use this tool ONLY when the user's query is specifically about credit cards."""
    logging.info("Calling credit_cards_specialised_agent")
    agent = Agent(system_prompt="You are an expert in Credit Cards, in the context of a Bank.")
    return agent


def initialize_agent():
    orchestrator = Agent(
        # model= we're using the model by default.
        tools=[debit_cards_specialised_agent, credit_cards_specialised_agent],
        system_prompt="You are a routing agent. Route each query to exactly one specialized agent. If the query is about debit cards, use the debit card agent. If it is about credit cards, use the credit card agent. If the topic is ambiguous, ask the user to clarify. Never call both agents for the same query.",
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
