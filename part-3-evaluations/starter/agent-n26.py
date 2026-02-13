"""
Strands Agents Workshop - Part 3: Evaluations
N26 Banking Assistant for simulation exercises.

This agent is already implemented - you'll use it in simulation_evaluation.py.
"""

from strands import Agent

agent = Agent(
    system_prompt="You are the helpful N26 assistant. You help customers with questions about N26 bank accounts, cards, and services.",
    callback_handler=None,
)

# Quick test
if __name__ == "__main__":
    result = agent("What are the benefits of the metal account?")
    print(result.message)
