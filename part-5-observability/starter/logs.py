import logging

from strands import Agent
from strands_tools import calculator

# TODO: Configure the root strands logger to DEBUG level
# Hint: Use logging.getLogger("strands").setLevel(...)

# TODO: Add a handler so you can see the logs in the console
# Hint: Use logging.basicConfig() with a StreamHandler and a format string

# Create an agent with the calculator tool
agent = Agent(tools=[calculator])
result = agent("What is 125 * 37?")
