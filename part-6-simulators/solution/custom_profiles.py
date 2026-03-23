"""
Strands Simulators: Custom Actor Profiles

https://strandsagents.com/docs/user-guide/evals-sdk/simulators/user_simulation/

This example shows how to define custom ActorProfile objects to simulate
specific user personas. Each profile has traits, context, and a goal that
shape how the simulated user interacts with the agent.
"""

from strands import Agent
from strands_evals import Case, Experiment, ActorSimulator
from strands_evals.evaluators import OutputEvaluator
from strands_evals.types.simulation import ActorProfile


# Define distinct user personas with different traits and goals
CUSTOMER_PROFILES = {
    "impatient_executive": ActorProfile(
        traits={
            "expertise_level": "novice",
            "communication_style": "direct",
            "patience_level": "low",
            "detail_preference": "low",
        },
        context="A busy CEO who wants fast answers. Doesn't have time for long explanations. "
        "Will get frustrated if the agent rambles or asks too many clarifying questions.",
        actor_goal="Get a quick, clear recommendation for a 3-day business trip destination "
        "with good conference facilities.",
    ),
    "detail_oriented_planner": ActorProfile(
        traits={
            "expertise_level": "advanced",
            "communication_style": "analytical",
            "patience_level": "high",
            "detail_preference": "high",
        },
        context="An experienced traveler who plans every trip meticulously. Wants specific "
        "details about costs, logistics, and alternatives. Will ask follow-up questions "
        "to get precise information.",
        actor_goal="Get a comprehensive breakdown of a two-week Italy itinerary including "
        "costs, transport options, and must-see attractions for each city.",
    ),
    "anxious_first_timer": ActorProfile(
        traits={
            "expertise_level": "novice",
            "communication_style": "casual",
            "patience_level": "medium",
            "detail_preference": "medium",
        },
        context="A 22-year-old who has never traveled abroad. Nervous about flying and "
        "navigating a foreign country alone. Needs reassurance and simple step-by-step guidance.",
        actor_goal="Feel confident about planning a first solo trip to Thailand, "
        "including visa, safety tips, and essential packing advice.",
    ),
}


def run_simulation(case: Case) -> str:
    """Run a simulation using a custom actor profile."""
    print(f"\n>>> Starting simulation: {case.name}")

    profile_key = case.metadata.get("customer_profile")
    profile = CUSTOMER_PROFILES[profile_key]

    # Create simulator with the custom profile and a tailored system prompt
    simulator = ActorSimulator(
        actor_profile=profile,
        initial_query=case.input,
        max_turns=5,
        system_prompt_template="""You are simulating a user with the following profile:
{actor_profile}

Guidelines:
- Stay in character based on your traits (patience, communication style, expertise)
- Ask follow-up questions naturally based on your goal
- Express satisfaction when your goal is achieved
- Include <stop/> when you feel your questions have been answered
""",
    )

    print(f">>> Profile: {profile_key}")
    print(f">>> Goal: {profile.actor_goal}")

    agent = Agent(
        system_prompt="You are a helpful travel assistant. Adapt your communication style "
        "to match the user — be concise with busy users, detailed with planners, "
        "and reassuring with nervous travelers.",
        callback_handler=None,
    )

    user_message = case.input
    agent_message = ""
    turn = 0

    while simulator.has_next() and turn < 5:
        turn += 1
        print(f"  Turn {turn} | User: {user_message[:80]}...")

        agent_response = agent(user_message)
        agent_message = str(agent_response)
        print(f"  Turn {turn} | Agent: {agent_message[:80]}...")

        user_result = simulator.act(agent_message)
        user_message = str(user_result.structured_output.message)

    print(f">>> Completed in {turn} turns\n")
    return f"Conversation completed in {turn} turns. Final response: {agent_message}"


test_cases = [
    Case[str, str](
        name="executive-quick-recommendation",
        input="I need a destination for a 3-day business trip next month. What do you suggest?",
        expected_output="Concise recommendation with a destination suited for business travel",
        metadata={
            "customer_profile": "impatient_executive",
            "task_description": "Busy executive gets a fast, actionable recommendation",
        },
    ),
    Case[str, str](
        name="planner-italy-itinerary",
        input="I'm planning a two-week trip to Italy. Can you help me build a detailed itinerary?",
        expected_output="Detailed multi-city Italy itinerary with costs and logistics",
        metadata={
            "customer_profile": "detail_oriented_planner",
            "task_description": "Detail-oriented planner gets a comprehensive Italy itinerary",
        },
    ),
    Case[str, str](
        name="first-timer-solo-travel",
        input="I've never been abroad before and I'm thinking about going to Thailand alone. "
        "I'm kind of nervous... where do I even start?",
        expected_output="Reassuring step-by-step guide for first-time solo travel to Thailand",
        metadata={
            "customer_profile": "anxious_first_timer",
            "task_description": "Anxious first-time traveler gets reassuring, practical guidance",
        },
    ),
]

evaluator = OutputEvaluator(
    rubric="""
    Evaluate the conversation considering the user persona:

    1. Persona Adaptation (0-0.4): Did the agent adapt its style to the user?
       - Concise for impatient users, detailed for planners, reassuring for anxious users
    2. Goal Achievement (0-0.3): Did the conversation address the user's specific goal?
    3. Conversation Quality (0-0.3): Was the multi-turn exchange natural and productive?

    Score 1.0 for excellent adaptation and goal fulfillment.
    Score 0.5-0.8 for good but imperfect persona matching.
    Score below 0.5 for failure to adapt or meet the user's needs.
    """,
    include_inputs=True,
)

experiment = Experiment[str, str](cases=test_cases, evaluators=[evaluator])

if __name__ == "__main__":
    print("=== Custom Actor Profile Simulation ===\n")

    reports = experiment.run_evaluations(run_simulation)

    print("\n=== Results ===")
    reports[0].run_display()

    experiment.to_file("custom_profiles_simulation")
    print("\nExperiment saved to ./custom_profiles_simulation.json")
