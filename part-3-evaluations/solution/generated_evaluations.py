"""
Strands Evaluations: ExperimentGenerator

Same as evaluations.py but uses ExperimentGenerator to auto-generate test cases.
https://strandsagents.com/latest/documentation/docs/user-guide/evals-sdk/experiment_generator/
"""

import asyncio
from strands_evals import Case
from strands_evals.generators import ExperimentGenerator
from strands_evals.evaluators import OutputEvaluator

from agent import agent


# Context describing the agent's capabilities
AGENT_CONTEXT = """
Math Assistant Agent

The agent helps users with mathematical calculations using a sum_calculator tool.

Capabilities:
- Add two numbers together using sum_calculator(a, b)
- Explain calculations clearly
- Handle positive, negative, and decimal numbers

Example interactions:
- "What is 5 + 3?" -> Returns 8
- "Add 10 and 20" -> Returns 30
- "Sum of -5 and 15" -> Returns 10
"""


def get_response(case: Case) -> str:
    """Get response from the agent for a given test case."""
    response = agent(case.input)
    return str(response)


async def main():
    """Generate test cases and run evaluations."""
    # Initialize the generator
    generator = ExperimentGenerator[str, str](
        input_type=str,
        output_type=str,
        include_expected_output=True,
    )

    # Generate experiment from context
    experiment = await generator.from_context_async(
        context=AGENT_CONTEXT,
        task_description="Math assistant that adds numbers using sum_calculator",
        num_cases=5,
        evaluator=OutputEvaluator,
    )

    print(f"Generated {len(experiment.cases)} test cases\n")
    for i, case in enumerate(experiment.cases):
        print(f"[{i+1}] {case.input} -> {case.expected_output}")

    # Run evaluations
    print("\n" + "=" * 50)
    reports = experiment.run_evaluations(get_response)
    reports[0].run_display()


if __name__ == "__main__":
    asyncio.run(main())
