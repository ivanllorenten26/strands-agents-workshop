# Part 3: Agent Evaluations

Learn how to evaluate AI agents using the `strands-agents-evals` framework. This module covers different evaluation strategies from simple output validation to complex multi-turn conversation simulations.

## 📚 Learning Objectives

By the end of this session, you will:

- ✅ Understand how to define test cases and run evaluation experiments
- ✅ Write custom rubrics for LLM-as-judge scoring with `OutputEvaluator`
- ✅ Validate agent tool usage with `TrajectoryEvaluator`
- ✅ Simulate multi-turn conversations with `ActorSimulator` and `ActorProfile`
- ✅ Auto-generate test cases using `ExperimentGenerator`

## 🛠️ Session Structure

### `/starter` Directory

Contains boilerplate code with TODOs for you to implement. Each file has the imports, structure, and hints — you fill in the evaluation logic.

### `/solution` Directory

Contains a complete, working implementation that you can reference if you get stuck or want to compare your approach.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- AWS account with Bedrock access

### Setup Instructions

1. Navigate to the starter directory:

```bash
cd part-3-evaluations/starter
```

2. Create and activate a virtual environment:

```bash
uv venv && source .venv/bin/activate
```

3. Install dependencies:

```bash
uv pip install -r requirements.txt
```

4. Review the starter code and look for TODOs in each file

### Running Your Evaluations

1. Output evaluation: `python output_evaluations.py`
2. Tool usage (trajectory) evaluation: `python tools_evaluations.py`
3. User simulation: `python simulation_evaluation.py`
4. Auto-generated test cases: `python generated_evaluations.py`

---

## ✏️ Exercises

### Exercise 1: `output_evaluations.py`

**Goal:** Define test cases and create an evaluator with a custom rubric.

**What to implement:**
- Add test cases using `Case[str, str]` with input, expected output, and metadata
- Create an `OutputEvaluator` with a rubric that scores accuracy, tool usage, and clarity

**Key concepts:**

```python
from strands_evals import Case, Experiment
from strands_evals.evaluators import OutputEvaluator

test_cases = [
    Case[str, str](
        name="simple-addition",
        input="What is 10 + 5?",
        expected_output="15",
    )
]

experiment = Experiment[str, str](cases=test_cases, evaluators=[OutputEvaluator()])
reports = experiment.run_evaluations(get_response)
```

### Exercise 2: `tools_evaluations.py`

**Goal:** Implement `get_response` to return both output AND tool trajectory.

**What to implement:**
- Use `tools_use_extractor.extract_agent_tools_used_from_messages(agent.messages)` to extract the tools used
- Return a dict with `"output"` and `"trajectory"` keys

**Key concepts:**

```python
from strands_evals.evaluators import TrajectoryEvaluator
from strands_evals.extractors import tools_use_extractor

trajectory = tools_use_extractor.extract_agent_tools_used_from_messages(agent.messages)

test_case = Case[str, str](
    name="math-operation",
    input="What is 10 + 5?",
    expected_trajectory=["sum_calculator"],
)
```

### Exercise 3: `simulation_evaluation.py`

**Goal:** Define customer profiles and implement a multi-turn simulation loop.

**What to implement:**
- Create `ActorProfile` entries in `CUSTOMER_PROFILES` with traits, context, and goals
- Implement `run_simulation` to create an `ActorSimulator`, loop with `has_next()` / `act()`, and return the result

**Key concepts:**

```python
from strands_evals import ActorSimulator
from strands_evals.types.simulation import ActorProfile

profile = ActorProfile(
    traits={
        "expertise_level": "intermediate",
        "communication_style": "professional",
    },
    context="A frequent traveler considering a premium account...",
    actor_goal="Get detailed info about travel insurance benefits",
)

simulator = ActorSimulator(
    actor_profile=profile,
    initial_query="Tell me about premium features",
    max_turns=5,
)
```

### Exercise 4: `generated_evaluations.py`

**Goal:** Write an `AGENT_CONTEXT` description so the LLM can auto-generate test cases.

**What to implement:**
- Describe your agent's capabilities, example interactions, and constraints in `AGENT_CONTEXT`

**Key concepts:**

```python
from strands_evals.generators import ExperimentGenerator

generator = ExperimentGenerator[str, str](
    input_type=str,
    output_type=str,
    include_expected_output=True,
)

experiment = await generator.from_context_async(
    context="Agent that adds numbers using sum_calculator...",
    task_description="Math assistant evaluation",
    num_cases=5,
    evaluator=OutputEvaluator,
)
```

---

## 📖 Key Concepts

### Evaluator Types

The `strands-agents-evals` framework provides evaluators that operate at different levels of granularity:

| Level           | Scope             | Use Case                           |
| --------------- | ----------------- | ---------------------------------- |
| `OUTPUT_LEVEL`  | Single response   | Quality of individual outputs      |
| `TRACE_LEVEL`   | Single turn       | Turn-by-turn conversation analysis |
| `SESSION_LEVEL` | Full conversation | End-to-end goal achievement        |

### Scoring Methods

For trajectory evaluation, the framework provides built-in scoring helpers:

| Method                   | Description                                    | Use Case                              |
| ------------------------ | ---------------------------------------------- | ------------------------------------- |
| `exact_match_scorer`     | Tools must match exactly in order              | Strict workflow validation            |
| `in_order_match_scorer`  | Expected tools appear in order (allows extras) | Flexible workflow with optional steps |
| `any_order_match_scorer` | All expected tools present (any order)         | When order doesn't matter             |

### Best Practices

1. **Start simple:** Begin with `OutputEvaluator` and manual test cases, then add complexity
2. **Use meaningful rubrics:** Clear, specific rubrics lead to better LLM-as-judge evaluations
3. **Cover edge cases:** Include negative numbers, empty inputs, error scenarios in test cases
4. **Save experiments:** Use `experiment.to_file()` to version and compare results over time
5. **Simulate real users:** Use `ActorProfile` traits that match your actual user personas

---

## 🔗 Further Reading

- [Strands Evals Documentation](https://strandsagents.com/latest/documentation/docs/user-guide/evals-sdk/quickstart/)
- [User Simulation Guide](https://strandsagents.com/latest/documentation/docs/user-guide/evals-sdk/simulators/user_simulation/)
- [Experiment Generator](https://strandsagents.com/latest/documentation/docs/user-guide/evals-sdk/experiment_generator/)
