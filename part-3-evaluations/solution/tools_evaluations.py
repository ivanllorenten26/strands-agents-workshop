"""
Strands Evaluations: tool usage evaluations

https://strandsagents.com/latest/documentation/docs/user-guide/evals-sdk/quickstart/#tool-usage-evaluation
"""
from strands_evals import Case, Experiment
from strands_evals.evaluators import TrajectoryEvaluator
from strands_evals.extractors import tools_use_extractor

# Import the production agent directly
from agent import agent


# Define your task function
def get_response(case: Case) -> str:
    response = agent(case.input)
    trajectory = tools_use_extractor.extract_agent_tools_used_from_messages(agent.messages)

    return {"output": str(response), "trajectory": trajectory}

# Create test cases for sum_calculator, using specific tool usage evaluator
test_cases = [
    Case[str, str](
        name="simple-addition",
        input="What is the sum of 10 + 5?",
        expected_trajectory=["sum_calculator"],
        metadata={"category": "math", "expected_tools": ["sum_calculator"]}
    ),
    Case[str, str](
        name="negative-numbers",
        input="What is -15 + 20?",
        expected_trajectory=["sum_calculator"],
        metadata={"category": "math", "expected_tools": ["sum_calculator"]}
    ),
    Case[str, str](
        name="zero-addition",
        input="Calculate 0 + 42",
        expected_trajectory=["sum_calculator"],
        metadata={"category": "math", "expected_tools": ["sum_calculator"]}
    ),
    Case[str, str](
        name="large-numbers",
        input="What is 9999 + 8888?",
        expected_trajectory=["sum_calculator"],
        metadata={"category": "math", "expected_tools": ["sum_calculator"]}
    ),
    Case[str, str](
        name="negative-result",
        input="Add -100 and -50",
        expected_trajectory=["sum_calculator"],
        metadata={"category": "math", "expected_tools": ["sum_calculator"]}
    )
]

# Create evaluator with custom rubric for sum_calculator
evaluator = TrajectoryEvaluator(
    rubric="""
    Evaluate the tool usage trajectory:
    1. Correct tool selection - Were the right tools chosen for the task?
    2. Proper sequence - Were tools used in a logical order?
    3. Efficiency - Were unnecessary tools avoided?

    Use the built-in scoring tools to verify trajectory matches:
    - exact_match_scorer for exact sequence matching
    - in_order_match_scorer for ordered subset matching  
    - any_order_match_scorer for unordered matching

    Score 1.0 if optimal tools used correctly.
    Score 0.5 if correct tools used but suboptimal sequence.
    Score 0.0 if wrong tools used or major inefficiencies.
    """,
    include_inputs=True
)

# Create and run experiment
experiment = Experiment[str, str](cases=test_cases, evaluators=[evaluator])
reports = experiment.run_evaluations(get_response)

# Display results
print("=== Tool Usage Evaluation Results ===")
reports[0].run_display()

# Save experiment
experiment.to_file("trajectory_evaluation")
print("\nExperiment saved to ./experiment_files/trajectory_evaluation.json")
