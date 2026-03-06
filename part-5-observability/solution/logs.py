import logging
import os

from strands import Agent
from strands.models import BedrockModel
from strands_tools import calculator

# Configure the root strands logger
logging.getLogger("strands").setLevel(logging.DEBUG)

# Add a handler to see the logs
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

# Create an agent with the calculator tool
model = BedrockModel(
    model_id=os.getenv("MODEL_ID"),
)


agent = Agent(
    model=model,
    tools=[calculator]
)
result = agent("What is 125 * 37?")
