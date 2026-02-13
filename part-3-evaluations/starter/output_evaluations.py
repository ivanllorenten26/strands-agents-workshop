"""
Strands Evaluations - Output Evaluation
https://strandsagents.com/latest/documentation/docs/user-guide/evals-sdk/quickstart/

Your task: Define test cases and create an evaluator with a custom rubric.
The experiment setup and execution is already implemented for you.
"""

from strands_evals import Case, Experiment
from strands_evals.evaluators import OutputEvaluator
from agent import agent


def get_response(case: Case) -> str:
    """Call the agent with the test case input."""
    response = agent(case.input)
    return str(response)


# TODO: Create test cases for sum_calculator
# Use Case[str, str](name, input, expected_output, metadata)
test_cases = [
    # Example:
    # Case[str, str](
    #     name="simple-addition",
    #     input="What is the sum of 10 + 5?",
    #     expected_output="15",
    #     metadata={"category": "basic_math"}
    # ),
]


# TODO: Create an OutputEvaluator with a rubric
# The rubric should explain how to score: 1.0 (correct), 0.5 (partial), 0.0 (wrong)
evaluator = None


def main():
    """Run the evaluation experiment."""
    if not test_cases:
        print("TODO: Add your test cases to the test_cases list!")
        return
    if not evaluator:
        print("TODO: Create your OutputEvaluator with a rubric!")
        return

    # Create and run the experiment
    experiment = Experiment[str, str](cases=test_cases, evaluators=[evaluator])
    reports = experiment.run_evaluations(get_response)

    # Display results
    print("=== Sum Calculator Evaluation Results ===")
    reports[0].run_display()

    # Save experiment
    experiment.to_file("sum_calculator_evaluation")
    print("\nExperiment saved to ./sum_calculator_evaluation.json")


if __name__ == "__main__":
    main()
