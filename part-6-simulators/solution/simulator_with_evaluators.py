"""
Strands Simulators: Full Integration with Trace-Based Evaluators

https://strandsagents.com/docs/user-guide/evals-sdk/simulators/

This example combines simulators with telemetry and trace-based evaluators to
perform comprehensive multi-turn evaluation. It collects OpenTelemetry spans
during the conversation and uses session-level evaluators (HelpfulnessEvaluator,
GoalSuccessRateEvaluator) alongside output-level evaluators.
"""

from strands import Agent
from strands_evals import Case, Experiment, ActorSimulator
from strands_evals.evaluators import HelpfulnessEvaluator, GoalSuccessRateEvaluator
from strands_evals.mappers import StrandsInMemorySessionMapper
from strands_evals.telemetry import StrandsEvalsTelemetry

# Setup in-memory telemetry to capture spans for trace-based evaluation
telemetry = StrandsEvalsTelemetry().setup_in_memory_exporter()
memory_exporter = telemetry.in_memory_exporter


def run_simulation(case: Case) -> dict:
    """Run a simulation and collect telemetry spans for trace-based evaluation."""
    print(f"\n>>> Starting simulation: {case.name}")

    # Create simulator from case metadata
    simulator = ActorSimulator.from_case_for_user_simulator(
        case=case,
        max_turns=8,
    )

    print(f">>> Goal: {simulator.actor_profile.actor_goal}")

    # Create agent with trace attributes for span correlation
    agent = Agent(
        system_prompt="You are a knowledgeable tech support agent. You help users "
        "troubleshoot software issues, explain technical concepts, and guide them "
        "through solutions step by step.",
        trace_attributes={
            "gen_ai.conversation.id": case.session_id,
            "session.id": case.session_id,
        },
        callback_handler=None,
    )

    # Run multi-turn conversation, collecting spans
    user_message = case.input
    agent_message = ""
    turn = 0

    while simulator.has_next():
        turn += 1
        print(f"  Turn {turn} | User: {user_message[:80]}...")

        agent_response = agent(user_message)
        agent_message = str(agent_response)
        print(f"  Turn {turn} | Agent: {agent_message[:80]}...")

        user_result = simulator.act(agent_message)
        user_message = str(user_result.structured_output.message)

    # Map collected spans to a session for trace-based evaluation
    all_spans = memory_exporter.get_finished_spans()
    mapper = StrandsInMemorySessionMapper()
    session = mapper.map_to_session(all_spans, session_id=case.session_id)

    print(f">>> Completed in {turn} turns, collected {len(all_spans)} spans\n")

    # Return both output and trajectory for the evaluators
    return {"output": agent_message, "trajectory": session}


# Test cases for a tech support agent
test_cases = [
    Case[str, str](
        name="git-merge-conflict",
        input="I'm getting a merge conflict in Git and I don't know how to fix it. "
        "Can you walk me through it?",
        expected_output="Step-by-step instructions for resolving a Git merge conflict",
        metadata={
            "task_description": "User successfully understands how to resolve "
            "Git merge conflicts after the conversation",
        },
    ),
    Case[str, str](
        name="python-virtual-env",
        input="My Python imports keep failing. I think it might be a virtual environment "
        "issue but I'm not sure what that means.",
        expected_output="Explanation of virtual environments and how to fix import issues",
        metadata={
            "task_description": "User understands what virtual environments are and "
            "can fix their Python import issues",
        },
    ),
    Case[str, str](
        name="docker-container-crash",
        input="My Docker container keeps crashing on startup. The logs say "
        "'exec format error'. What does that mean?",
        expected_output="Explanation of exec format error and how to fix platform mismatch",
        metadata={
            "task_description": "User understands the cause of the exec format error "
            "and knows how to rebuild for the correct platform",
        },
    ),
]

# Combine session-level evaluators for comprehensive assessment
evaluators = [
    HelpfulnessEvaluator(),
    GoalSuccessRateEvaluator(),
]

experiment = Experiment(cases=test_cases, evaluators=evaluators)

if __name__ == "__main__":
    print("=== Simulator with Trace-Based Evaluators ===\n")

    reports = experiment.run_evaluations(run_simulation)

    print("\n=== Results ===")
    for report in reports:
        report.run_display()

    experiment.to_file("simulator_with_evaluators")
    print("\nExperiment saved to ./simulator_with_evaluators.json")
