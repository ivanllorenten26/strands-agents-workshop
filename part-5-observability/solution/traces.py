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

# Initialize the Strands telemetry object
strands_telemetry = StrandsTelemetry()

# Always enable console exporter so we can see traces in the terminal
strands_telemetry.setup_console_exporter()

# If Langfuse credentials are set, configure the OTLP exporter to send traces there.
# Langfuse exposes an OTLP-compatible endpoint at <host>/api/public/otel/v1/traces
langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY")
langfuse_host = os.getenv("LANGFUSE_HOST") or os.getenv("LANGFUSE_BASE_URL", "http://localhost:3000")

if langfuse_public_key and langfuse_secret_key:
    print(f"Langfuse credentials detected — exporting traces to {langfuse_host}")
    auth_token = base64.b64encode(f"{langfuse_public_key}:{langfuse_secret_key}".encode("utf-8")).decode("ascii")
    strands_telemetry.setup_otlp_exporter(
        endpoint=f"{langfuse_host}/api/public/otel/v1/traces",
        headers={
            "Authorization": f"Basic {auth_token}",
        },
    )
else:
    print("No Langfuse credentials found — traces will only be printed to the console.")
    print("Set LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, and optionally LANGFUSE_HOST to enable Langfuse.")

# --- Agent Setup ---

model = BedrockModel(
    model_id=os.getenv("MODEL_ID", "us.anthropic.claude-sonnet-4-20250514"),
)

agent = Agent(
    model=model,
    tools=[calculator],
    # Custom trace attributes add business context to every span
    trace_attributes={
        "session.id": "workshop-traces-demo",
        "user.id": "workshop-participant",
        "tags": ["strands-workshop", "part-5-observability"],
    },
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
