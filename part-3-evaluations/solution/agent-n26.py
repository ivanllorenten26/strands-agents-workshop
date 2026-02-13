"""
Strands Evaluations
https://strandsagents.com/latest/documentation/docs/user-guide/evals-sdk/quickstart/

Strands Evaluation is a framework for evaluating AI agents and LLM applications.
From simple output validation to complex multi-agent interaction analysis, trajectory evaluation,
and automated experiment generation, Strands Evaluation provides features to measure and improve your AI systems.

What Strands Evaluation Provides:
- Multiple Evaluation Types: Output evaluation, trajectory analysis, tool usage assessment, and interaction evaluation
- Dynamic Simulators: Multi-turn conversation simulation with realistic user behavior and goal-oriented interactions
- LLM-as-a-Judge: Built-in evaluators using language models for sophisticated assessment with structured scoring
- Trace-based Evaluation: Analyze agent behavior through OpenTelemetry execution traces
- Automated Experiment Generation: Generate comprehensive test suites from context descriptions
- Custom Evaluators: Extensible framework for domain-specific evaluation logic
- Experiment Management: Save, load, and version your evaluation experiments with JSON serialization
- Built-in Scoring Tools: Helper functions for exact, in-order, and any-order trajectory matching

"""

from strands import Agent

agent = Agent(system_prompt="You are the helpful N26 assistant.", callback_handler=None)

result = agent("What are the benefits of the metal account?")

print(result.message)
