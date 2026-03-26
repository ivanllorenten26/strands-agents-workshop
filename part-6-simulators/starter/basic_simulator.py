"""
Strands Simulators: Basic User Simulation

https://strandsagents.com/docs/user-guide/evals-sdk/simulators/

Your task: Use ActorSimulator.from_case_for_user_simulator() to automatically
generate a user persona from a test case and run a multi-turn conversation.
"""

from strands import Agent
from strands_evals import Case, Experiment, ActorSimulator
from strands_evals.evaluators import OutputEvaluator


def run_simulation(case: Case) -> str:
    """
    Run a multi-turn conversation between a simulated user and an agent.

    TODO: Implement the simulation:
    1. Create a simulator with ActorSimulator.from_case_for_user_simulator(case=case, max_turns=5)
    2. Create an Agent with a travel assistant system prompt and callback_handler=None
    3. Loop while simulator.has_next():
       - agent_response = agent(user_message)
       - user_result = simulator.act(str(agent_response))
       - user_message = str(user_result.structured_output.message)
    4. Return a summary string with the final agent response
    """
    print(f"\n>>> Starting simulation: {case.name}")

    # Your code here
    pass


# TODO: Define test cases with input and metadata containing a "task_description"
# The simulator auto-generates user personas from the metadata.
# Example:
# Case[str, str](
#     name="weekend-trip",
#     input="I'm looking for a fun weekend getaway in Europe.",
#     expected_output="Recommendations for European weekend destinations",
#     metadata={
#         "task_description": "User gets helpful destination recommendations",
#     },
# ),
test_cases = []

# TODO: Create an OutputEvaluator with a rubric scoring helpfulness,
# goal achievement, and conversation flow
evaluator = None


def main():
    if not test_cases:
        print("TODO: Add your test cases!")
        return
    if not evaluator:
        print("TODO: Create your OutputEvaluator with a rubric!")
        return

    experiment = Experiment[str, str](cases=test_cases, evaluators=[evaluator])

    print("=== Basic User Simulation ===\n")
    reports = experiment.run_evaluations(run_simulation)

    print("\n=== Results ===")
    reports[0].run_display()

    experiment.to_file("basic_simulation")
    print("\nExperiment saved to ./basic_simulation.json")


if __name__ == "__main__":
    main()
