"""
Strands Evaluations - Output Evaluation
https://strandsagents.com/latest/documentation/docs/user-guide/evals-sdk/quickstart/

Your task: Define test cases and create an evaluator with a custom rubric.
The experiment setup and execution is already implemented for you.
"""
from strands_evals import Case, Experiment
from strands_evals.evaluators import OutputEvaluator

# Import the production agent directly
from agent import agent

# Define your task function
def get_response(case: Case) -> str:
    response = agent(case.input)
    return str(response)

# Create test cases for sum_calculator
test_cases = [
    Case[str, str](
        name="simple-addition",
        input="What is the sum of 10 + 5?",
        expected_output="15",
        metadata={"category": "basic_math"}
    ),
    Case[str, str](
        name="negative-numbers",
        input="What is -15 + 20?",
        expected_output="5",
        metadata={"category": "edge_cases"}
    ),
    Case[str, str](
        name="zero-addition",
        input="Calculate 0 + 42",
        expected_output="42",
        metadata={"category": "edge_cases"}
    ),
    Case[str, str](
        name="large-numbers",
        input="What is 9999 + 8888?",
        expected_output="18887",
        metadata={"category": "basic_math"}
    ),
    Case[str, str](
        name="negative-result",
        input="Add -100 and -50",
        expected_output="-150",
        metadata={"category": "edge_cases"}
    )
]

# Create evaluator with custom rubric for sum_calculator
evaluator = OutputEvaluator(
    rubric="""
    Evaluate the mathematical response based on:
    1. Accuracy - Is the calculation result correct?
    2. Tool Usage - Did the agent properly use the sum_calculator tool?
    3. Clarity - Is the answer presented clearly?

    Score 1.0 if the calculation is correct and well-presented.
    Score 0.5 if the calculation is correct but presentation is unclear.
    Score 0.0 if the calculation is incorrect.
    """,
    include_inputs=True
)

# Create and run experiment
experiment = Experiment[str, str](cases=test_cases, evaluators=[evaluator])
reports = experiment.run_evaluations(get_response)

# Display results
print("=== Sum Calculator Evaluation Results ===")
reports[0].run_display()

# Save experiment for later analysis
experiment.to_file("sum_calculator_evaluation")
print("\nExperiment saved to ./sum_calculator_evaluation.json")
