"""Traces example using OpenTelemetry (OTEL) with console export and Langfuse integration.

To run with console export only:
    python traces.py

To run with a local Langfuse instance:
    1. Start Langfuse locally (see docker-compose.yml or https://langfuse.com/self-hosting)
    2. Create a project in Langfuse at http://localhost:3000 and grab your API keys
    3. Set the environment variables:
        export LANGFUSE_PUBLIC_KEY="pk-lf-..."
        export LANGFUSE_SECRET_KEY="sk-lf-..."
    4. Run: python traces.py
"""

import os
import base64

from strands import Agent
from strands.models import BedrockModel
from strands.telemetry import StrandsTelemetry
from strands_tools import calculator

# --- Telemetry Setup ---

# TODO: Initialize the Strands telemetry object
# Hint: strands_telemetry = StrandsTelemetry()

# TODO: Enable the console exporter so traces appear in the terminal
# Hint: strands_telemetry.setup_console_exporter()

# TODO: If Langfuse credentials are set, configure the OTLP exporter.
# Langfuse exposes an OTLP-compatible endpoint at <host>/api/public/otel/v1/traces
# Steps:
#   1. Read LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY from env vars
#   2. Build a Basic auth token: base64(public_key:secret_key)
#   3. Call strands_telemetry.setup_otlp_exporter(endpoint=..., headers={"Authorization": f"Basic {auth_token}"})
# If no credentials are found, just print a message saying traces will only go to the console.

# --- Agent Setup ---

model = BedrockModel(
    model_id=os.getenv("MODEL_ID", "us.anthropic.claude-sonnet-4-20250514"),
)

# TODO: Create an Agent with the model, calculator tool, and custom trace_attributes
# trace_attributes add business context to every span. Example:
#   trace_attributes={
#       "session.id": "workshop-traces-demo",
#       "user.id": "workshop-participant",
#       "tags": ["strands-workshop", "part-5-observability"],
#   }
agent = Agent(
    model=model,
    tools=[calculator],
    # Add trace_attributes here
)

# --- Run the Agent ---

result = agent("What is 42 * 38 + 17?")

# Print a summary of what was captured
print()
print("########## Trace Summary ##########")
print(f"Total tokens: {result.metrics.accumulated_usage['totalTokens']}")
print(f"Execution time: {sum(result.metrics.cycle_durations):.2f} seconds")
print(f"Cycles count: {result.metrics.cycle_count}")
print(f"Tools used: {list(result.metrics.tool_metrics.keys())}")
