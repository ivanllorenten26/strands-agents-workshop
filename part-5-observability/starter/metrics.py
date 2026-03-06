import os

from strands import Agent
from strands.models import BedrockModel
from strands_tools import calculator

model = BedrockModel(
    model_id=os.getenv("MODEL_ID"),
)

agent = Agent(
    model=model,
    tools=[calculator]
)

result = agent("What is the square root of 144?")

# TODO: Access and print metrics from the AgentResult object
# The `result` object has a `.metrics` attribute with useful data.
#
# Print the following:
#   - Total tokens used (hint: result.metrics.accumulated_usage['totalTokens'])
#   - Execution time in seconds (hint: sum of result.metrics.cycle_durations)
#   - Number of cycles (hint: result.metrics.cycle_count)
#   - Tools used (hint: result.metrics.tool_metrics.keys())
print()
print("########## Metrics #########")
# Your code here
