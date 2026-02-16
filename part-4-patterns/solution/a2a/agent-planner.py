from strands import Agent
from strands.multiagent.a2a import A2AServer
from strands_tools.a2a_client import A2AClientToolProvider

provider = A2AClientToolProvider(
    known_agent_urls=["http://127.0.0.1:9001"],
)

planner = Agent(
    name="Planner",
    description="Creates plans and asks Critic to review them.",
    tools=provider.tools,
    system_prompt=(
        "You are a planner.\n"
        "When asked to create a plan, do:\n"
        "1) Draft the plan\n"
        "2) Call the Critic agent (via A2A tool) to review it\n"
        "3) Produce a final improved plan based on the critique\n"
    ),
)

server = A2AServer(agent=planner)
print("Planner running on http://127.0.0.1:9000")
server.serve(host="127.0.0.1", port=9000)
