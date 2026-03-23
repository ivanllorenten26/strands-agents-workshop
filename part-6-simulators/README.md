# Part 6: Simulators

Learn how to use the Strands Evals SDK simulators to automatically test your agents with realistic, multi-turn conversations. Simulators actively participate in conversations with your agent, adapting their responses dynamically — unlike static evaluators that passively score single outputs.

## Learning Objectives

By the end of this session, you will:

- Understand the difference between simulators and evaluators
- Use `ActorSimulator.from_case_for_user_simulator()` for auto-generated user personas
- Define custom `ActorProfile` objects to simulate specific user types
- Combine simulators with trace-based evaluators (`HelpfulnessEvaluator`, `GoalSuccessRateEvaluator`)
- Collect OpenTelemetry spans during simulated conversations for session-level evaluation

## Session Structure

### `/starter` Directory

Contains boilerplate code with TODOs for you to implement. Each file has the imports, structure, and hints — you fill in the simulation logic.

### `/solution` Directory

Contains a complete, working implementation that you can reference if you get stuck or want to compare your approach.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- AWS account with Bedrock access

### Setup Instructions

1. Navigate to the starter directory:

```bash
cd part-6-simulators/starter
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv && source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up your AWS credentials:

```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
```

5. Review the starter code and look for TODOs in each file

### Running the Examples

1. Basic simulation: `python basic_simulator.py`
2. Custom profiles: `python custom_profiles.py`
3. Simulator with evaluators: `python simulator_with_evaluators.py`

---

## Exercises

### Exercise 1: `basic_simulator.py`

**Goal:** Use auto-generated user personas to run multi-turn conversations.

**What to implement:**
- Create a simulator with `ActorSimulator.from_case_for_user_simulator()`
- Implement the conversation loop using `simulator.has_next()` and `simulator.act()`
- Define test cases with `metadata["task_description"]` for persona generation

**Key concepts:**

```python
from strands_evals import ActorSimulator, Case

simulator = ActorSimulator.from_case_for_user_simulator(case=case, max_turns=5)

user_message = case.input
while simulator.has_next():
    agent_response = agent(user_message)
    user_result = simulator.act(str(agent_response))
    user_message = str(user_result.structured_output.message)
```

### Exercise 2: `custom_profiles.py`

**Goal:** Define custom user personas to test how the agent adapts its style.

**What to implement:**
- Create `ActorProfile` entries with traits, context, and goals
- Use `ActorSimulator` directly with custom profiles
- Customize the `system_prompt_template` for simulation behavior

**Key concepts:**

```python
from strands_evals.types.simulation import ActorProfile

profile = ActorProfile(
    traits={
        "expertise_level": "novice",
        "communication_style": "direct",
        "patience_level": "low",
    },
    context="A busy executive who wants fast answers...",
    actor_goal="Get a quick recommendation for a business trip.",
)

simulator = ActorSimulator(
    actor_profile=profile,
    initial_query=case.input,
    max_turns=5,
    system_prompt_template="You are simulating a user with: {actor_profile}\n...",
)
```

### Exercise 3: `simulator_with_evaluators.py`

**Goal:** Combine simulators with telemetry and trace-based evaluators.

**What to implement:**
- Set up `StrandsEvalsTelemetry` with an in-memory exporter
- Create an agent with `trace_attributes` for span correlation
- Map collected spans to a session with `StrandsInMemorySessionMapper`
- Use `HelpfulnessEvaluator` and `GoalSuccessRateEvaluator`

**Key concepts:**

```python
from strands_evals.telemetry import StrandsEvalsTelemetry
from strands_evals.mappers import StrandsInMemorySessionMapper
from strands_evals.evaluators import HelpfulnessEvaluator, GoalSuccessRateEvaluator

telemetry = StrandsEvalsTelemetry().setup_in_memory_exporter()
memory_exporter = telemetry.in_memory_exporter

# After conversation loop:
all_spans = memory_exporter.get_finished_spans()
mapper = StrandsInMemorySessionMapper()
session = mapper.map_to_session(all_spans, session_id=case.session_id)

return {"output": agent_message, "trajectory": session}
```

---

## Key Concepts

### Simulators vs. Evaluators

| Aspect | Simulators | Evaluators |
|--------|-----------|------------|
| Role | Actively participate in conversations | Passively assess outputs |
| Scope | Multi-turn, dynamic | Single output, static |
| Adaptation | Respond based on agent behavior | Fixed criteria |
| Use together | Generate conversations | Score them |

### ActorSimulator Configuration

| Parameter | Description |
|-----------|-------------|
| `max_turns` | Maximum conversation turns (3-5 for simple, 8-15 for complex) |
| `actor_profile` | Custom `ActorProfile` with traits, context, and goals |
| `initial_query` | First user message (used with custom profiles) |
| `system_prompt_template` | Template controlling simulation behavior |

### ActorProfile Traits

Common trait keys used in profiles:

| Trait | Example Values |
|-------|---------------|
| `expertise_level` | `"novice"`, `"intermediate"`, `"advanced"` |
| `communication_style` | `"casual"`, `"professional"`, `"direct"`, `"analytical"` |
| `patience_level` | `"low"`, `"medium"`, `"high"` |
| `detail_preference` | `"low"`, `"medium"`, `"high"` |

### Best Practices

1. **Write specific task descriptions** in case metadata — the simulator uses them to generate behavior
2. **Set appropriate turn limits** — 3-5 for simple tasks, 8-15 for complex ones
3. **Combine evaluators** — use `HelpfulnessEvaluator` + `GoalSuccessRateEvaluator` for comprehensive assessment
4. **Log conversations** for debugging and analysis
5. **Use custom profiles** that match your real user personas

---

## Further Reading

- [Strands Simulators Overview](https://strandsagents.com/docs/user-guide/evals-sdk/simulators/)
- [User Simulation Guide](https://strandsagents.com/docs/user-guide/evals-sdk/simulators/user_simulation/)
- [Evaluators Documentation](https://strandsagents.com/docs/user-guide/evals-sdk/evaluators/)
- [Evals SDK Quickstart](https://strandsagents.com/docs/user-guide/evals-sdk/quickstart/)
