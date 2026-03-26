"""
Strands Simulators: Basic User Simulation

https://strandsagents.com/docs/user-guide/evals-sdk/simulators/

A minimal example showing how to use ActorSimulator.from_case_for_user_simulator()
to automatically generate a user persona from a test case and run a multi-turn
conversation with an agent.
"""

from strands import Agent
from strands_evals import Case, Experiment, ActorSimulator
from strands_evals.evaluators import OutputEvaluator


def run_simulation(case: Case) -> str:
    """Run a multi-turn conversation between a simulated user and an agent."""
    print(f"\n>>> Starting simulation: {case.name}")

    # Create simulator from the case — profile is auto-generated from metadata
    simulator = ActorSimulator.from_case_for_user_simulator(
        case=case,
        max_turns=5,
    )

    print(f">>> Actor goal: {simulator.actor_profile.actor_goal}")

    # Create the agent under test
    agent = Agent(
        system_prompt="You are a helpful travel assistant. You help users plan trips, "
        "find destinations, and provide travel advice.",
        callback_handler=None,
    )

    # Multi-turn conversation loop
    user_message = case.input
    agent_message = ""
    turn = 0

    while simulator.has_next():
        turn += 1
        print(f"  Turn {turn} | User: {user_message[:80]}...")

        # Agent responds to the user
        agent_response = agent(user_message)
        agent_message = str(agent_response)
        print(f"  Turn {turn} | Agent: {agent_message[:80]}...")

        # Simulator generates the next user message
        user_result = simulator.act(agent_message)
        user_message = str(user_result.structured_output.message)

    print(f">>> Simulation completed in {turn} turns\n")
    return f"Conversation completed in {turn} turns. Final response: {agent_message}"


# Define test cases — the simulator auto-generates user personas from metadata
test_cases = [
    Case[str, str](
        name="weekend-trip-planning",
        input="I'm looking for a fun weekend getaway in Europe. Any suggestions?",
        expected_output="Recommendations for European weekend destinations with practical details",
        metadata={
            "task_description": "User gets helpful destination recommendations with "
            "enough detail to start planning a weekend trip",
        },
    ),
    Case[str, str](
        name="budget-travel-advice",
        input="I want to travel to Japan but I'm on a tight budget. How can I save money?",
        expected_output="Budget tips for traveling in Japan including transport, food, and accommodation",
        metadata={
            "task_description": "User receives practical budget-saving tips for Japan "
            "covering accommodation, transport, and food",
        },
    ),
]

# Evaluate the conversation quality
evaluator = OutputEvaluator(
    rubric="""
    Evaluate the simulated conversation based on:

    1. Helpfulness (0-0.5): Did the agent provide useful, actionable travel advice?
    2. Goal Achievement (0-0.3): Did the conversation help the user with their request?
    3. Conversation Flow (0-0.2): Was the multi-turn exchange natural and coherent?

    Score 1.0 for excellent conversations that fully address the user's needs.
    Score 0.5-0.8 for good conversations with minor gaps.
    Score below 0.5 for conversations that failed to help the user.
    """,
    include_inputs=True,
)

experiment = Experiment[str, str](cases=test_cases, evaluators=[evaluator])

if __name__ == "__main__":
    print("=== Basic User Simulation ===\n")

    reports = experiment.run_evaluations(run_simulation)

    print("\n=== Results ===")
    reports[0].run_display()

    experiment.to_file("basic_simulation")
    print("\nExperiment saved to ./basic_simulation.json")
