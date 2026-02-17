from strands import Agent
from strands.multiagent.a2a import A2AServer

critic = Agent(
    name="Critic",
    description="Reviews plans and suggests improvements.",
    system_prompt=(
        "You are a strict but helpful critic.\n"
        "Given a plan, respond with:\n"
        "1) Risks\n2) Missing steps\n3) Improvements\n"
        "Be concise."
    ),
)

# TODO: Create an A2AServer to expose the critic agent over HTTP.
# Hint: Use A2AServer with:
#   - agent: the critic agent
#   - host: "127.0.0.1"
#   - port: 9001
#   - http_url: "http://127.0.0.1:9001"
# Then print a message and call server.serve()
