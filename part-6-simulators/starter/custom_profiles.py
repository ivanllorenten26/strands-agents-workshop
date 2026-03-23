"""
Strands Simulators: Custom Actor Profiles

https://strandsagents.com/docs/user-guide/evals-sdk/simulators/user_simulation/

Your task: Define custom ActorProfile objects for different user personas and
use them with ActorSimulator to test how the agent adapts its communication style.
"""

from strands import Agent
from strands_evals import Case, Experiment, ActorSimulator
from strands_evals.evaluators import OutputEvaluator
from strands_evals.types.simulation import ActorProfile


# TODO: Define at least two customer profiles with different personas.
# Each ActorProfile needs: traits (dict), context (str), actor_goal (str)
# Example:
# "impatient_executive": ActorProfile(
#     traits={
#         "expertise_level": "novice",
#         "communication_style": "direct",
#         "patience_level": "low",
#         "detail_preference": "low",
#     },
#     context="A busy CEO who wants fast answers...",
#     actor_goal="Get a quick recommendation for a business trip destination.",
# ),
CUSTOMER_PROFILES = {}


def run_simulation(case: Case) -> str:
    """
    Run a simulation using a custom actor profile.

    TODO: Implement the simulation:
    1. Get the profile key from case.metadata["customer_profile"]
    2. Look up the ActorProfile in CUSTOMER_PROFILES
    3. Create an ActorSimulator with:
       - actor_profile=profile
       - initial_query=case.input
       - max_turns=5
       - system_prompt_template (customize the simulation behavior)
    4. Create an Agent
    5. Loop while simulator.has_next():
       - agent_response = agent(user_message)
       - user_result = simulator.act(str(agent_response))
       - user_message = str(user_result.structured_output.message)
    6. Return a summary string
    """
    print(f"\n>>> Starting simulation: {case.name}")

    # Your code here
    pass


# TODO: Create test cases that reference your CUSTOMER_PROFILES via metadata.
# Each case should have metadata={"customer_profile": "<profile_key>", "task_description": "..."}
test_cases = []

# TODO: Create an OutputEvaluator with a rubric that scores persona adaptation,
# goal achievement, and conversation quality
evaluator = None


def main():
    if not CUSTOMER_PROFILES:
        print("TODO: Define your CUSTOMER_PROFILES!")
        return
    if not test_cases:
        print("TODO: Add your test cases!")
        return
    if not evaluator:
        print("TODO: Create your OutputEvaluator!")
        return

    experiment = Experiment[str, str](cases=test_cases, evaluators=[evaluator])

    print("=== Custom Actor Profile Simulation ===\n")
    reports = experiment.run_evaluations(run_simulation)

    print("\n=== Results ===")
    reports[0].run_display()

    experiment.to_file("custom_profiles_simulation")
    print("\nExperiment saved to ./custom_profiles_simulation.json")


if __name__ == "__main__":
    main()
