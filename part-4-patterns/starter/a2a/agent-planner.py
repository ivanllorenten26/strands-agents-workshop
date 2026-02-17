from strands import Agent
from strands.multiagent.a2a import A2AServer
from strands_tools.a2a_client import A2AClientToolProvider

# TODO: Create an A2AClientToolProvider that knows about the critic agent.
# Hint: Use A2AClientToolProvider with known_agent_urls=["http://127.0.0.1:9001"]

planner = Agent(
    name="Planner",
    description="Creates plans and asks Critic to review them.",
    # TODO: Add the tools parameter using provider.tools
    system_prompt=(
        "You are a planner.\n"
        "When asked to create a plan, do:\n"
        "1) Draft the plan\n"
        "2) Call the Critic agent (via A2A tool) to review it\n"
        "3) Produce a final improved plan based on the critique\n"
    ),
)

# TODO: Create an A2AServer to expose the planner agent over HTTP.
# Hint: Use A2AServer with:
#   - agent: the planner agent
#   - host: "127.0.0.1"
#   - port: 9002
#   - http_url: "http://127.0.0.1:9002"
# Then print a message and call server.serve()
