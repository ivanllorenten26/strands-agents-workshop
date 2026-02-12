"""
Strands Evaluations: User Simulation

https://strandsagents.com/latest/documentation/docs/user-guide/evals-sdk/simulators/user_simulation/

User simulators enable automated multi-turn conversation testing by simulating
realistic user behavior. The simulator acts as a virtual user with specific
goals and personas, allowing you to test how your agent handles extended
conversations without manual intervention.
"""

from strands import Agent
from strands_evals import Case, Experiment, ActorSimulator
from strands_evals.evaluators import OutputEvaluator
from strands_evals.types.simulation import ActorProfile


# Custom actor profiles for different N26 customer personas
CUSTOMER_PROFILES = {
    "tech_savvy_traveler": ActorProfile(
        traits={
            "expertise_level": "intermediate",
            "communication_style": "professional",
            "patience_level": "high",
            "detail_preference": "high",
        },
        context="A 32-year-old software developer living in Berlin who travels frequently for work. "
        "Currently has N26 You but considering upgrading to Metal for better travel benefits. "
        "Values detailed information and likes to compare features before making financial decisions.",
        actor_goal="Get comprehensive information about N26 Metal benefits, especially travel insurance "
        "and partner offers, to decide if the upgrade is worth it for my lifestyle.",
    ),
    "busy_professional": ActorProfile(
        traits={
            "expertise_level": "novice",
            "communication_style": "direct",
            "patience_level": "low",
            "detail_preference": "low",
        },
        context="A 45-year-old marketing executive who doesn't have much time to research banking products. "
        "Wants quick, clear answers without unnecessary details. Currently uses a traditional bank "
        "and heard about N26 from colleagues.",
        actor_goal="Quickly understand the main differences between free and Metal accounts "
        "to decide if N26 is right for me.",
    ),
    "price_conscious_student": ActorProfile(
        traits={
            "expertise_level": "novice",
            "communication_style": "casual",
            "patience_level": "medium",
            "detail_preference": "medium",
        },
        context="A 24-year-old graduate student in Munich on a tight budget. Interested in the Metal card "
        "for the status symbol but needs to justify the cost. Looking for concrete value propositions.",
        actor_goal="Find out exactly how much Metal costs and whether the benefits justify "
        "the price for someone on a student budget.",
    ),
}


# Define the task function that runs the simulation
def run_simulation(case: Case) -> str:
    """Run a multi-turn conversation simulation."""
    print(f"\n>>> Starting simulation for case: {case.name}")

    try:
        # Get custom profile from metadata, or use default from case
        profile_key = case.metadata.get("customer_profile") if case.metadata else None

        if profile_key and profile_key in CUSTOMER_PROFILES:
            # Use custom ActorSimulator with defined profile
            profile = CUSTOMER_PROFILES[profile_key]
            user_sim = ActorSimulator(
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
            print(f">>> Using custom profile: {profile_key}")
        else:
            # Fallback to automatic profile generation
            user_sim = ActorSimulator.from_case_for_user_simulator(
                case=case, max_turns=5
            )
            print(">>> Using auto-generated profile")

        print(f">>> Simulator created, has_next: {user_sim.has_next()}")
        print(f">>> Actor goal: {user_sim.actor_profile.actor_goal}")

        # Create the N26 agent (without callback handler for evaluation)
        agent = Agent(
            system_prompt="You are the helpful N26 assistant. You help customers with questions about N26 bank accounts, cards, and services.",
            callback_handler=None,
        )

        # Run multi-turn conversation
        user_message = case.input
        conversation_log = []
        agent_message = ""
        turn = 0

        while user_sim.has_next() and turn < 5:
            turn += 1
            print(f">>> Turn {turn}: User says: {user_message[:50]}...")

            # Agent responds
            agent_response = agent(user_message)
            agent_message = str(agent_response)
            conversation_log.append({"role": "agent", "message": agent_message})
            print(f">>> Agent responded: {agent_message[:100]}...")

            # User simulator generates next message
            user_result = user_sim.act(agent_message)
            user_message = str(user_result.structured_output.message)
            conversation_log.append({"role": "user", "message": user_message})
            print(f">>> Simulator next: {user_message[:50]}...")

        result = f"Conversation completed in {len(conversation_log) // 2} turns. Final agent response: {agent_message}"
        print(f">>> Result: {result[:100]}...")
        return result
    except Exception as e:
        import traceback

        print(f">>> ERROR: {type(e).__name__}: {e}")
        traceback.print_exc()
        return f"Error: {e}"


# Test cases with different initial user messages and customer personas
test_cases = [
    # Tech-savvy traveler: Already has N26 You, wants detailed info about Metal upgrade
    Case[str, str](
        name="travel-benefits-inquiry",
        input="Hi, I currently have N26 You and I'm considering upgrading to Metal. "
        "I travel a lot for work - can you tell me about the travel insurance coverage?",
        expected_output="N26 Metal includes comprehensive travel insurance with medical coverage, "
        "trip cancellation, flight delay compensation, and luggage protection",
        metadata={
            "category": "account_inquiry",
            "customer_profile": "tech_savvy_traveler",
            "task_description": "Customer receives detailed information about N26 Metal travel insurance "
            "benefits to evaluate if the upgrade is worthwhile for frequent travelers",
        },
    ),
    # Busy professional: Wants quick, direct comparison without fluff
    Case[str, str](
        name="quick-comparison",
        input="I don't have much time - just tell me the main differences between free and Metal.",
        expected_output="Free account: no fee, basic features. Metal: monthly fee, metal card, "
        "insurance, partner offers, priority support",
        metadata={
            "category": "account_comparison",
            "customer_profile": "busy_professional",
            "task_description": "Customer gets a concise summary of free vs Metal differences "
            "without excessive details",
        },
    ),
    # Price-conscious student: Budget focused, needs to justify the cost
    Case[str, str](
        name="student-pricing",
        input="Hey, I'm a student and money is tight. How much is Metal per month "
        "and is it really worth it for someone on a budget?",
        expected_output="N26 Metal costs €16.90 per month. For students, the value depends on "
        "travel frequency and use of partner discounts",
        metadata={
            "category": "pricing",
            "customer_profile": "price_conscious_student",
            "task_description": "Customer receives honest pricing information and advice "
            "on whether Metal makes sense for a student budget",
        },
    ),
]

# Create evaluator for conversation quality
evaluator = OutputEvaluator(
    rubric="""
    Evaluate the multi-turn conversation based on:
    
    1. Helpfulness (0-0.4): Did the agent provide useful information about N26 Metal?
       - Mentioned key benefits (insurance, metal card, cashback, etc.)
       - Provided pricing information when asked
       - Addressed customer concerns
    
    2. Conversation Flow (0-0.3): Was the conversation natural and coherent?
       - Agent understood follow-up questions
       - Responses were contextually appropriate
       - Conversation progressed logically
    
    3. Goal Achievement (0-0.3): Did the conversation help the user reach their goal?
       - User received enough information to make a decision
       - Key questions were answered
       - Conversation reached a natural conclusion
    
    Score 1.0 if the conversation was excellent across all dimensions.
    Score 0.5-0.8 for good conversations with minor issues.
    Score below 0.5 for conversations that failed to help the user.
    """,
    include_inputs=True,
)

# Create and run experiment
experiment = Experiment[str, str](cases=test_cases, evaluators=[evaluator])

if __name__ == "__main__":
    print("=== N26 Agent User Simulation Evaluation ===\n")

    reports = experiment.run_evaluations(run_simulation)

    # Display results
    print("\n=== Simulation Results ===")
    reports[0].run_display()

    # Save experiment
    experiment.to_file("simulation_evaluation")
    print("\nExperiment saved to ./simulation_evaluation.json")
