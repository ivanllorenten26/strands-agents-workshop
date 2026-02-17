import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from strands import Agent


def run_workflow(topic: str):
    researcher = Agent(system_prompt="Find key info.")
    analyst = Agent(system_prompt="Extract insights from research.")
    writer = Agent(system_prompt="Write a polished report.")

    researcher_output = researcher(f"Research: {topic}")
    analyst_output = analyst(f"Analyze: {researcher_output}")
    return writer(f"Write report from: {analyst_output}")


def main():
    """
    Main entry point for the agent application.
    """
    print("Running the workflow with a predefined topic...")
    result = run_workflow("Instant payments regulation in Europe.")
    print(result)


if __name__ == "__main__":
    main()
