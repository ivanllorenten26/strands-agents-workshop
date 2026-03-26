"""
Strands Simulators: Full Integration with Trace-Based Evaluators

https://strandsagents.com/docs/user-guide/evals-sdk/simulators/

Your task: Combine simulators with telemetry and trace-based evaluators to
perform comprehensive multi-turn evaluation. Collect OpenTelemetry spans and
use session-level evaluators (HelpfulnessEvaluator, GoalSuccessRateEvaluator).
"""

from strands import Agent
from strands_evals import Case, Experiment, ActorSimulator
from strands_evals.evaluators import HelpfulnessEvaluator, GoalSuccessRateEvaluator
from strands_evals.mappers import StrandsInMemorySessionMapper
from strands_evals.telemetry import StrandsEvalsTelemetry

# TODO: Setup in-memory telemetry to capture spans for trace-based evaluation
# 1. Create a StrandsEvalsTelemetry instance and call .setup_in_memory_exporter()
# 2. Store the in_memory_exporter for later use
# telemetry = StrandsEvalsTelemetry().setup_in_memory_exporter()
# memory_exporter = telemetry.in_memory_exporter
telemetry = None
memory_exporter = None


def run_simulation(case: Case) -> dict:
    """
    Run a simulation and collect telemetry spans for trace-based evaluation.

    TODO: Implement the full simulation with telemetry:
    1. Create a simulator with ActorSimulator.from_case_for_user_simulator(case, max_turns=8)
    2. Create an Agent with:
       - A tech support system prompt
       - trace_attributes with "gen_ai.conversation.id" and "session.id" set to case.session_id
       - callback_handler=None
    3. Run the multi-turn conversation loop
    4. After the loop, map spans to a session:
       - all_spans = memory_exporter.get_finished_spans()
       - mapper = StrandsInMemorySessionMapper()
       - session = mapper.map_to_session(all_spans, session_id=case.session_id)
    5. Return a dict with "output" (final agent message) and "trajectory" (session)
    """
    print(f"\n>>> Starting simulation: {case.name}")

    # Your code here
    pass


# TODO: Define test cases for a tech support agent.
# Each case needs input, expected_output, and metadata with "task_description".
test_cases = []

# TODO: Create evaluators list with HelpfulnessEvaluator() and GoalSuccessRateEvaluator()
evaluators = []


def main():
    if not telemetry:
        print("TODO: Setup telemetry!")
        return
    if not test_cases:
        print("TODO: Add your test cases!")
        return
    if not evaluators:
        print("TODO: Add your evaluators!")
        return

    experiment = Experiment(cases=test_cases, evaluators=evaluators)

    print("=== Simulator with Trace-Based Evaluators ===\n")
    reports = experiment.run_evaluations(run_simulation)

    print("\n=== Results ===")
    for report in reports:
        report.run_display()

    experiment.to_file("simulator_with_evaluators")
    print("\nExperiment saved to ./simulator_with_evaluators.json")


if __name__ == "__main__":
    main()
