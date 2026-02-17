# Part 4: Multi-Agent Patterns

Learn how to orchestrate multiple agents using different architectural patterns. This module covers five patterns that let you compose agents for increasingly complex workflows — from simple chaining to distributed agent-to-agent communication.

## 📚 Learning Objectives

By the end of this session, you will:

- ✅ Understand how to wrap an agent as a reusable tool for an orchestrator
- ✅ Chain agents sequentially in a workflow pipeline
- ✅ Build a directed acyclic graph (DAG) of agents using `GraphBuilder`
- ✅ Coordinate autonomous agents with handoffs using `Swarm`
- ✅ Expose agents over HTTP and communicate between them using the A2A protocol

## 🛠️ Session Structure

### `/starter` Directory

Contains boilerplate code with TODOs for you to implement. Each file has the imports, structure, and hints — you fill in the multi-agent orchestration logic.

### `/solution` Directory

Contains a complete, working implementation that you can reference if you get stuck or want to compare your approach.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- AWS account with Bedrock access in eu-central-1 region
- Teleport access configured for AWS credentials

### Setup Instructions

1. Navigate to the starter directory:

```bash
cd part-4-patterns/starter
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

### Running the Exercises

1. Agents as Tools: `python agents-as-tools.py`
2. Workflow (sequential chaining): `python workflow.py`
3. Graph (DAG): `python graph.py`
4. Swarm (autonomous handoffs): `python swarm.py`
5. Agent-to-Agent (A2A): `bash run-a2a.sh`

---

## ✏️ Exercises

### Exercise 1: `agents-as-tools.py`

**Goal:** Create a specialised agent and expose it as a tool for an orchestrator agent.

**What to implement:**
- Define a function decorated with `@tool` that returns an `Agent` instance
- Pass that tool to the orchestrator agent via the `tools=` parameter

**Key concepts:**

```python
from strands import Agent, tool

@tool
def cards_specialised_agent():
    return Agent(system_prompt="You are an expert in Cards, in the context of a Bank.")

orchestrator = Agent(
    tools=[cards_specialised_agent],
    system_prompt="Route queries to specialized agents...",
)
```

### Exercise 2: `workflow.py`

**Goal:** Chain three agents sequentially — researcher, analyst, and writer — passing each output to the next.

**What to implement:**
- Call the researcher agent with the topic
- Feed the researcher's output into the analyst
- Feed the analyst's output into the writer
- Return the writer's final output

**Key concepts:**

```python
researcher_output = researcher(f"Research: {topic}")
analyst_output = analyst(f"Analyze: {researcher_output}")
result = writer(f"Write report from: {analyst_output}")
```

### Exercise 3: `graph.py`

**Goal:** Build a directed acyclic graph of agents using `GraphBuilder`.

**What to implement:**
- Add four agent nodes: research, analysis, fact_check, report
- Define edges so research fans out to analysis and fact_check, then both converge into report
- Set the entry point and execution timeout
- Build and return the graph

**Key concepts:**

```python
from strands.multiagent import GraphBuilder

builder = GraphBuilder()
builder.add_node(agent, "label")
builder.add_edge("from_label", "to_label")
builder.set_entry_point("label")
graph = builder.build()
```

### Exercise 4: `swarm.py`

**Goal:** Create a swarm of autonomous agents that can hand off work to each other.

**What to implement:**
- Instantiate a `Swarm` with a list of agents, an entry point, and configuration parameters

**Key concepts:**

```python
from strands.multiagent import Swarm

swarm = Swarm(
    [coder, researcher, reviewer, architect],
    entry_point=researcher,
    max_handoffs=20,
    max_iterations=20,
    execution_timeout=900.0,
    node_timeout=300.0,
)
```

### Exercise 5: Agent-to-Agent (A2A)

**Goal:** Expose agents as HTTP services and have them communicate using the A2A protocol.

This exercise spans three files:

| File | What to implement |
|------|-------------------|
| `a2a/agent-critic.py` | Create an `A2AServer` wrapping the critic agent on port 9001 |
| `a2a/agent-planner.py` | Create an `A2AClientToolProvider` to discover the critic, then expose the planner on port 9002 |
| `agent-to-agent-a2a.py` | Discover the planner's agent card, create a client, send a message, and print the response |

**Key concepts:**

```python
from strands.multiagent.a2a import A2AServer
from strands_tools.a2a_client import A2AClientToolProvider

# Server side
server = A2AServer(agent=my_agent, host="127.0.0.1", port=9001, http_url="http://127.0.0.1:9001")
server.serve()

# Client side (connecting to another agent)
provider = A2AClientToolProvider(known_agent_urls=["http://127.0.0.1:9001"])
agent = Agent(tools=provider.tools, ...)
```

Run all three together with:

```bash
bash run-a2a.sh
```

---

## 📖 Key Concepts

### Pattern Comparison

| Pattern | Coordination | Communication | Best For |
|---------|-------------|---------------|----------|
| **Agents as Tools** | Orchestrator calls sub-agents | Function call | Simple routing / delegation |
| **Workflow** | Sequential, hard-coded | Output passed as input | Linear pipelines |
| **Graph** | DAG with fan-out / fan-in | Managed by GraphBuilder | Parallel stages with dependencies |
| **Swarm** | Autonomous handoffs | Agents decide who goes next | Open-ended, collaborative tasks |
| **A2A** | Distributed over HTTP | A2A protocol | Microservice-style, cross-process agents |

### When to Use What

- **Agents as Tools** — You have a clear orchestrator and a few specialists. Simple and easy to reason about.
- **Workflow** — The pipeline is fixed and linear: step A then step B then step C.
- **Graph** — You need parallel execution with convergence (e.g., research fans out to analysis + fact-checking, then merges into a report).
- **Swarm** — The work is exploratory and agents should decide dynamically who handles the next step.
- **A2A** — Agents run as independent services, possibly in different processes or machines.

---

## 🔗 Further Reading

- [Multi-Agent Patterns Overview](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent-systems/agents-as-tools/)
- [Graph Builder](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent-systems/graph/)
- [Swarm](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent-systems/swarm/)
- [A2A Protocol](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent-systems/a2a/)
