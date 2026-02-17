import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from strands import Agent


def run_workflow(topic: str):
    researcher = Agent(system_prompt="Find key info.")
    analyst = Agent(system_prompt="Extract insights from research.")
    writer = Agent(system_prompt="Write a polished report.")

    # TODO: Chain the agents together sequentially.
    # 1. Call the researcher agent with the topic
    # 2. Pass the researcher's output to the analyst
    # 3. Pass the analyst's output to the writer
    # 4. Return the writer's output
    # Hint: output = agent(f"prompt: {previous_output}")
    pass


def main():
    """
    Main entry point for the agent application.
    """
    print("Running the workflow with a predefined topic...")
    result = run_workflow("Instant payments regulation in Europe.")
    print(result)


if __name__ == "__main__":
    main()
