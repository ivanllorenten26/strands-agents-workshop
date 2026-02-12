"""
Strands Evaluations - Tool Usage (Trajectory) Evaluation
https://strandsagents.com/latest/documentation/docs/user-guide/evals-sdk/quickstart/#tool-usage-evaluation

Your task: Implement get_response to return both output AND trajectory.
This verifies the agent uses the correct tools.
"""

from strands_evals import Case, Experiment
from strands_evals.evaluators import TrajectoryEvaluator
from strands_evals.extractors import tools_use_extractor
from agent import agent


def get_response(case: Case) -> dict:
    """
    Call the agent and extract tool usage trajectory.

    TODO: Return a dict with "output" and "trajectory" keys.
    Use tools_use_extractor.extract_agent_tools_used_from_messages(agent.messages)
    to get the list of tools that were called.
    """
    # Your code here
    pass


# Test cases with expected tool trajectory
test_cases = [
    Case[str, str](
        name="simple-addition",
        input="What is the sum of 10 + 5?",
        expected_trajectory=["sum_calculator"],
        metadata={"category": "math"},
    ),
    Case[str, str](
        name="negative-numbers",
        input="What is -15 + 20?",
        expected_trajectory=["sum_calculator"],
        metadata={"category": "math"},
    ),
    Case[str, str](
        name="large-numbers",
        input="What is 9999 + 8888?",
        expected_trajectory=["sum_calculator"],
        metadata={"category": "math"},
    ),
]


evaluator = TrajectoryEvaluator(
    rubric="""
    Evaluate the tool usage trajectory:
    1. Correct tool selection - Did the agent use sum_calculator?
    2. Efficiency - Were unnecessary tools avoided?

    Score 1.0 if the correct tool was used.
    Score 0.0 if wrong tools or no tools used.
    """,
    include_inputs=True,
)


def main():
    """Run the trajectory evaluation."""
    # Create and run experiment
    experiment = Experiment[str, str](cases=test_cases, evaluators=[evaluator])
    reports = experiment.run_evaluations(get_response)

    # Display results
    print("=== Tool Usage Evaluation Results ===")
    reports[0].run_display()

    # Save experiment
    experiment.to_file("trajectory_evaluation")


if __name__ == "__main__":
    main()
