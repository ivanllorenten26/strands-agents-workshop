# Part 3: Agent Evaluations

Learn how to evaluate AI agents using the `strands-agents-evals` framework. This module covers different evaluation strategies from simple output validation to complex multi-turn conversation simulations.

## Quick Start

```bash
cd starter
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
python evaluations.py
```

---

## Evaluation Files Index

| File                                                          | Purpose                                        | Key Components                               |
| ------------------------------------------------------------- | ---------------------------------------------- | -------------------------------------------- |
| [evaluations.py](solution/evaluations.py)                     | Basic output evaluation with manual test cases | `Case`, `Experiment`, `OutputEvaluator`      |
| [tools_evaluations.py](solution/tools_evaluations.py)         | Tool usage trajectory evaluation               | `TrajectoryEvaluator`, `tools_use_extractor` |
| [simulation_evaluation.py](solution/simulation_evaluation.py) | Multi-turn conversation simulation             | `ActorSimulator`, `ActorProfile`             |
| [generated_evaluations.py](solution/generated_evaluations.py) | Auto-generated test cases                      | `ExperimentGenerator`                        |

### evaluations.py

**What it does:** Evaluates agent responses against expected outputs using manually defined test cases.

**Key concepts:**

- Define test cases with `Case[str, str]` specifying input, expected output, and metadata
- Use `OutputEvaluator` with a custom rubric for LLM-as-judge scoring
- Run experiments and display results with `experiment.run_evaluations()`

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

### tools_evaluations.py

**What it does:** Validates that the agent uses the correct tools in the right order.

**Key concepts:**

- Extract tool usage from agent messages with `tools_use_extractor`
- Define `expected_trajectory` in test cases
- Use `TrajectoryEvaluator` to compare actual vs expected tool usage

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

### simulation_evaluation.py

**What it does:** Runs multi-turn conversations with a simulated user to test agent behavior over extended interactions.

**Key concepts:**

- `ActorSimulator` simulates a user with specific goals and personas
- Define custom `ActorProfile` with traits, context, and goals
- Test how agents handle follow-up questions and conversation flow

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

### generated_evaluations.py

**What it does:** Automatically generates test cases from a context description instead of writing them manually.

**Key concepts:**

- Describe your agent's capabilities in a context string
- `ExperimentGenerator` creates diverse test cases with expected outputs
- Useful for quickly building comprehensive test suites

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

## Evaluator Types

The `strands-agents-evals` framework provides evaluators that operate at different levels of granularity:

| Level           | Scope             | Use Case                           |
| --------------- | ----------------- | ---------------------------------- |
| `OUTPUT_LEVEL`  | Single response   | Quality of individual outputs      |
| `TRACE_LEVEL`   | Single turn       | Turn-by-turn conversation analysis |
| `SESSION_LEVEL` | Full conversation | End-to-end goal achievement        |

### Response Quality Evaluators

#### OutputEvaluator

**Level:** `OUTPUT_LEVEL`  
**Purpose:** Flexible LLM-based evaluation with custom rubrics.

**When to use:** Assess any subjective quality (safety, relevance, tone, accuracy).

```python
from strands_evals.evaluators import OutputEvaluator

evaluator = OutputEvaluator(
    rubric="""
    Score 1.0 if the response:
    - Directly answers the user's question
    - Provides accurate information
    - Uses appropriate tone

    Score 0.5 if partially meets criteria
    Score 0.0 if fails to meet criteria
    """,
    include_inputs=True
)
```

#### HelpfulnessEvaluator

**Level:** `TRACE_LEVEL`  
**Purpose:** Evaluate response helpfulness from user perspective.

**When to use:** Measure user satisfaction and response utility.

```python
from strands_evals.evaluators import HelpfulnessEvaluator

evaluator = HelpfulnessEvaluator()
```

#### FaithfulnessEvaluator

**Level:** `TRACE_LEVEL`  
**Purpose:** Assess factual accuracy and groundedness.

**When to use:** Verify responses are truthful and well-supported.

```python
from strands_evals.evaluators import FaithfulnessEvaluator

evaluator = FaithfulnessEvaluator()
```

### Tool Usage Evaluators

#### ToolSelectionEvaluator

**Level:** `TRACE_LEVEL`  
**Purpose:** Evaluate whether correct tools were selected.

**When to use:** Assess tool choice accuracy in multi-tool scenarios.

```python
from strands_evals.evaluators import ToolSelectionEvaluator

evaluator = ToolSelectionEvaluator()
```

#### ToolParameterEvaluator

**Level:** `TRACE_LEVEL`  
**Purpose:** Evaluate accuracy of tool parameters.

**When to use:** Verify correct parameter values for tool calls.

```python
from strands_evals.evaluators import ToolParameterEvaluator

evaluator = ToolParameterEvaluator()
```

### Conversation Flow Evaluators

#### TrajectoryEvaluator

**Level:** `SESSION_LEVEL`  
**Purpose:** Assess sequence of actions and tool usage patterns.

**When to use:** Evaluate multi-step reasoning and workflow adherence.

```python
from strands_evals.evaluators import TrajectoryEvaluator

evaluator = TrajectoryEvaluator(
    rubric="""
    Evaluate tool usage:
    1. Correct tools selected?
    2. Logical order?
    3. No unnecessary calls?

    Score 1.0 for optimal usage.
    Score 0.0 for wrong tools.
    """,
    include_inputs=True
)

# In your test case:
Case[str, str](
    input="Calculate 5 + 3",
    expected_trajectory=["sum_calculator"],
)
```

#### InteractionsEvaluator

**Level:** `SESSION_LEVEL`  
**Purpose:** Analyze conversation patterns and interaction quality.

**When to use:** Assess conversation flow and engagement patterns.

```python
from strands_evals.evaluators import InteractionsEvaluator

evaluator = InteractionsEvaluator()
```

### Goal Achievement Evaluators

#### GoalSuccessRateEvaluator

**Level:** `SESSION_LEVEL`  
**Purpose:** Determine if user goals were successfully achieved.

**When to use:** Measure end-to-end task completion success.

```python
from strands_evals.evaluators import GoalSuccessRateEvaluator

evaluator = GoalSuccessRateEvaluator()
```

### Custom Evaluators

**Purpose:** Create domain-specific evaluation logic for requirements not covered by built-in evaluators.

```python
from strands_evals.evaluators import Evaluator

class CustomEvaluator(Evaluator):
    def evaluate(self, data):
        # Your custom evaluation logic
        score = calculate_custom_metric(data.expected_output, data.output)
        return EvaluationResult(score=score, reasoning="...")
```

---

## Combining Evaluators

Assess different aspects comprehensively by combining multiple evaluators:

```python
evaluators = [
    HelpfulnessEvaluator(),      # User experience
    FaithfulnessEvaluator(),     # Accuracy
    ToolSelectionEvaluator(),    # Tool usage
    GoalSuccessRateEvaluator()   # Success rate
]

experiment = Experiment(cases=test_cases, evaluators=evaluators)
```

---

## Scoring Methods

For trajectory evaluation, the framework provides built-in scoring helpers:

| Method                   | Description                                    | Use Case                              |
| ------------------------ | ---------------------------------------------- | ------------------------------------- |
| `exact_match_scorer`     | Tools must match exactly in order              | Strict workflow validation            |
| `in_order_match_scorer`  | Expected tools appear in order (allows extras) | Flexible workflow with optional steps |
| `any_order_match_scorer` | All expected tools present (any order)         | When order doesn't matter             |

---

## Best Practices

1. **Start simple:** Begin with `OutputEvaluator` and manual test cases, then add complexity
2. **Use meaningful rubrics:** Clear, specific rubrics lead to better LLM-as-judge evaluations
3. **Cover edge cases:** Include negative numbers, empty inputs, error scenarios in test cases
4. **Save experiments:** Use `experiment.to_file()` to version and compare results over time
5. **Simulate real users:** Use `ActorProfile` traits that match your actual user personas

---

## Further Reading

- [Strands Evals Documentation](https://strandsagents.com/latest/documentation/docs/user-guide/evals-sdk/quickstart/)
- [User Simulation Guide](https://strandsagents.com/latest/documentation/docs/user-guide/evals-sdk/simulators/user_simulation/)
- [Experiment Generator](https://strandsagents.com/latest/documentation/docs/user-guide/evals-sdk/experiment_generator/)
