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

# Access metrics through the AgentResult
print()
print("########## Metrics #########")
print(f"Total tokens: {result.metrics.accumulated_usage['totalTokens']}")
print(f"Execution time: {sum(result.metrics.cycle_durations):.2f} seconds")
print(f"Cycles count: {result.metrics.cycle_count} times")
print(f"Tools used: {list(result.metrics.tool_metrics.keys())}")
