"""
Strands Evaluations
https://strandsagents.com/latest/documentation/docs/user-guide/evals-sdk/quickstart/

Strands Evaluation is a framework for evaluating AI agents and LLM applications.
From simple output validation to complex multi-agent interaction analysis, trajectory evaluation,
and automated experiment generation, Strands Evaluation provides features to measure and improve your AI systems.

What Strands Evaluation Provides:
- Multiple Evaluation Types: Output evaluation, trajectory analysis, tool usage assessment, and interaction evaluation
- Dynamic Simulators: Multi-turn conversation simulation with realistic user behavior and goal-oriented interactions
- LLM-as-a-Judge: Built-in evaluators using language models for sophisticated assessment with structured scoring
- Trace-based Evaluation: Analyze agent behavior through OpenTelemetry execution traces
- Automated Experiment Generation: Generate comprehensive test suites from context descriptions
- Custom Evaluators: Extensible framework for domain-specific evaluation logic
- Experiment Management: Save, load, and version your evaluation experiments with JSON serialization
- Built-in Scoring Tools: Helper functions for exact, in-order, and any-order trajectory matching

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
print("\nExperiment saved to ./experiment_files/sum_calculator_evaluation.json")
