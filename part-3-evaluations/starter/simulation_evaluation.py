"""
Strands Evaluations - User Simulation
https://strandsagents.com/latest/documentation/docs/user-guide/evals-sdk/simulators/user_simulation/

Your task: Define customer profiles and implement the simulation loop.
This tests multi-turn conversations with simulated users.
"""

from strands import Agent
from strands_evals import Case, Experiment, ActorSimulator
from strands_evals.evaluators import OutputEvaluator
from strands_evals.types.simulation import ActorProfile


# TODO: Define customer profiles with different personas
# Each ActorProfile needs: traits (dict), context (str), actor_goal (str)
CUSTOMER_PROFILES = {
    # Example:
    # "tech_savvy_user": ActorProfile(
    #     traits={
    #         "expertise_level": "intermediate",
    #         "communication_style": "professional",
    #         "patience_level": "high",
    #     },
    #     context="A software developer who wants detailed information...",
    #     actor_goal="Get comprehensive information about the product.",
    # ),
}


def run_simulation(case: Case) -> str:
    """
    Run a multi-turn conversation simulation.

    TODO: Implement the simulation loop:
    1. Get profile from case.metadata["customer_profile"]
    2. Create ActorSimulator with that profile
    3. Create an Agent
    4. Loop while simulator.has_next():
       - agent_response = agent(user_message)
       - user_result = simulator.act(str(agent_response))
       - user_message = str(user_result.structured_output.message)
    5. Return the final result
    """
    print(f"\n>>> Starting simulation: {case.name}")

    # Your code here
    pass


# Test cases - will use your CUSTOMER_PROFILES
test_cases = [
    Case[str, str](
        name="product-inquiry",
        input="Hi, I'd like to learn about your premium features.",
        expected_output="Information about premium features",
        metadata={
            "customer_profile": "tech_savvy_user",  # Must match a key in CUSTOMER_PROFILES
            "task_description": "User receives detailed product information",
        },
    ),
]


def main():
    """Run the simulation evaluation."""
    if not CUSTOMER_PROFILES:
        print("TODO: Define your CUSTOMER_PROFILES!")
        return

    evaluator = OutputEvaluator()
    experiment = Experiment[str, str](cases=test_cases, evaluators=[evaluator])
    reports = experiment.run_evaluations(run_simulation)

    print("\n=== Simulation Results ===")
    reports[0].run_display()


if __name__ == "__main__":
    main()
