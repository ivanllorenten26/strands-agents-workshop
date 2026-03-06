# Part 5: Observability

Learn how to monitor and debug AI agents using built-in metrics, structured logging, and distributed tracing with OpenTelemetry. This module covers three pillars of observability — metrics, logs, and traces — and shows how to visualize them with Langfuse.

## 📚 Learning Objectives

By the end of this session, you will:

- ✅ Understand the three pillars of observability: metrics, logs, and traces
- ✅ Extract built-in metrics from agent results (tokens, latency, cycles, tool usage)
- ✅ Configure structured logging for the Strands framework
- ✅ Set up OpenTelemetry tracing with `StrandsTelemetry`
- ✅ Export traces to a local Langfuse instance via the OTLP protocol
- ✅ Add custom trace attributes for session and user context

## 🛠️ Session Structure

### `/starter` Directory

Contains boilerplate code with TODOs for you to implement. Each file has the imports, structure, and hints — you fill in the observability logic.

### `/solution` Directory

Contains a complete, working implementation that you can reference if you get stuck or want to compare your approach.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- AWS account with Bedrock access
- Docker and Docker Compose (for running Langfuse locally)

### Setup Instructions

1. Navigate to the starter directory:

```bash
cd part-5-observability/starter
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv && source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up AWS credentials via Teleport:

```bash
# Use Teleport to get temporary AWS credentials
# Copy the export commands provided by Teleport and run them:
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_CA_BUNDLE="/path/to/ca-bundle.pem"
export HTTPS_PROXY="http://127.0.0.1:port"
```

5. Review the starter code and look for TODOs in each file

### Running the Examples

1. Agent metrics: `python metrics.py`
2. Structured logging: `python logs.py`
3. OpenTelemetry traces: `python traces.py`

---

## ✏️ Exercises

### Exercise 1: `metrics.py`

**Goal:** Extract and display built-in metrics from an agent execution result.

**What to implement:**
- Create a `BedrockModel` and an `Agent` with the `calculator` tool
- Run a query and access the `result.metrics` object
- Print token usage, execution time, cycle count, and tools used

**Key concepts:**

```python
from strands import Agent
from strands.models import BedrockModel
from strands_tools import calculator

model = BedrockModel(model_id=os.getenv("MODEL_ID"))
agent = Agent(model=model, tools=[calculator])

result = agent("What is the square root of 144?")

# Access metrics through the AgentResult
print(f"Total tokens: {result.metrics.accumulated_usage['totalTokens']}")
print(f"Execution time: {sum(result.metrics.cycle_durations):.2f} seconds")
print(f"Cycles count: {result.metrics.cycle_count}")
print(f"Tools used: {list(result.metrics.tool_metrics.keys())}")
```

### Exercise 2: `logs.py`

**Goal:** Configure structured logging for the Strands framework to see internal agent activity.

**What to implement:**
- Set the `strands` logger to `DEBUG` level
- Configure a `StreamHandler` with a readable format
- Create an agent and run a query to observe the log output

**Key concepts:**

```python
import logging

# Configure the root strands logger
logging.getLogger("strands").setLevel(logging.DEBUG)

# Add a handler to see the logs
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

agent = Agent(tools=[calculator])
result = agent("What is 125 * 37?")
```

### Exercise 3: `traces.py`

**Goal:** Set up OpenTelemetry tracing with console export and optional Langfuse integration.

**What to implement:**
- Initialize `StrandsTelemetry` and configure the console exporter
- Detect Langfuse credentials from environment variables and set up the OTLP exporter
- Create an agent with custom `trace_attributes` for session and user context
- Run a query and print a trace summary from the result metrics

**Key concepts:**

```python
from strands.telemetry import StrandsTelemetry

# Initialize telemetry
strands_telemetry = StrandsTelemetry()
strands_telemetry.setup_console_exporter()

# Optional: configure OTLP exporter for Langfuse
strands_telemetry.setup_otlp_exporter(
    endpoint=f"{langfuse_host}/api/public/otel/v1/traces",
    headers={"Authorization": f"Basic {auth_token}"},
)

# Add custom trace attributes to the agent
agent = Agent(
    model=model,
    tools=[calculator],
    trace_attributes={
        "session.id": "workshop-traces-demo",
        "user.id": "workshop-participant",
        "tags": ["strands-workshop", "part-5-observability"],
    },
)
```

---

## 🐳 Running Langfuse Locally

The `solution/` directory includes a `docker-compose.yml` that spins up a full Langfuse stack (web UI, worker, PostgreSQL, ClickHouse, MinIO, Redis).

1. Start the stack:

```bash
cd part-5-observability/solution
docker compose up -d
```

2. Open the Langfuse UI at [http://localhost:3000](http://localhost:3000)

3. Create a project and copy your API keys

4. Export the credentials before running `traces.py`:

```bash
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_BASE_URL="http://localhost:3000"
```

5. Run the traces example and check the Langfuse UI for your traces:

```bash
python traces.py
```

---

## 📖 Key Concepts

### The Three Pillars of Observability

| Pillar | What It Captures | Strands Integration |
|--------|-----------------|---------------------|
| **Metrics** | Quantitative measurements (tokens, latency, cycles) | `result.metrics` on every `AgentResult` |
| **Logs** | Discrete events and internal agent activity | Python `logging` module with `strands` logger |
| **Traces** | End-to-end request flow across agent cycles and tool calls | `StrandsTelemetry` with OpenTelemetry exporters |

### Agent Metrics

Every `AgentResult` exposes a `metrics` object with:

| Field | Description |
|-------|-------------|
| `accumulated_usage['totalTokens']` | Total tokens consumed (input + output) |
| `cycle_durations` | List of durations per agent cycle (sum for total time) |
| `cycle_count` | Number of reasoning-action cycles the agent executed |
| `tool_metrics` | Dict of tool names to their execution metrics |

### OpenTelemetry Exporters

| Exporter | Use Case |
|----------|----------|
| **Console** | Quick debugging — prints spans to stdout |
| **OTLP** | Production — sends spans to any OTLP-compatible backend (Langfuse, Jaeger, Grafana Tempo, etc.) |

### Trace Attributes

Custom `trace_attributes` on the `Agent` constructor let you tag every span with business context:

- `session.id` — correlate traces across a conversation
- `user.id` — identify the user who triggered the request
- `tags` — free-form labels for filtering and grouping

---

## 🔗 Further Reading

- [Strands Observability Documentation](https://strandsagents.com/latest/user-guide/concepts/agents/agent-observability/)
- [OpenTelemetry Python SDK](https://opentelemetry.io/docs/languages/python/)
- [Langfuse Self-Hosting Guide](https://langfuse.com/self-hosting)
- [Langfuse OTEL Integration](https://langfuse.com/docs/opentelemetry/introduction)
