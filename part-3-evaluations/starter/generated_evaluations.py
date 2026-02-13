"""
Strands Evaluations - ExperimentGenerator
https://strandsagents.com/latest/documentation/docs/user-guide/evals-sdk/experiment_generator/

Your task: Write an AGENT_CONTEXT description so the LLM can generate test cases.
This is the same as evaluations.py but test cases are auto-generated!
"""

import asyncio
from strands_evals import Case
from strands_evals.generators import ExperimentGenerator
from strands_evals.evaluators import OutputEvaluator
from agent import agent


# TODO: Describe what your agent does
# Include: capabilities, example inputs/outputs, constraints
AGENT_CONTEXT = """
# Write your agent description here
# The better the description, the better the generated test cases!
"""


def get_response(case: Case) -> str:
    """Call the agent with the test case input."""
    response = agent(case.input)
    return str(response)


async def main():
    """Generate test cases and run evaluations."""
    if not AGENT_CONTEXT.strip() or AGENT_CONTEXT.startswith("#"):
        print("TODO: Write your AGENT_CONTEXT description!")
        return

    # Initialize the generator
    generator = ExperimentGenerator[str, str](
        input_type=str,
        output_type=str,
        include_expected_output=True,
    )

    # Generate experiment from your context
    print("Generating test cases from context...")
    experiment = await generator.from_context_async(
        context=AGENT_CONTEXT,
        task_description="Math assistant that adds numbers",
        num_cases=5,
        evaluator=OutputEvaluator,
    )

    # Show what was generated
    print(f"\nGenerated {len(experiment.cases)} test cases:\n")
    for i, case in enumerate(experiment.cases):
        print(f"[{i+1}] {case.input} -> {case.expected_output}")

    # Run evaluations
    print("\n" + "=" * 50)
    reports = experiment.run_evaluations(get_response)
    reports[0].run_display()


if __name__ == "__main__":
    asyncio.run(main())
