"""
Strands Agents Workshop - Part 3: Evaluations
Base agent with sum_calculator tool for evaluation exercises.

This agent is already implemented - you'll use it to test your evaluations.
"""

from strands import Agent, tool


@tool
def sum_calculator(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


agent = Agent(tools=[sum_calculator])

# Quick test
if __name__ == "__main__":
    result = agent("What is the sum of 10 + 5?")
    print(result.message)
