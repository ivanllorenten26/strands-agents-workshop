import asyncio
import logging
import httpx

from a2a.client import A2ACardResolver, ClientConfig, ClientFactory
from a2a.types import Message, Part, Role, TextPart
from uuid import uuid4

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 300
PLANNER_BASE_URL = "http://127.0.0.1:9002"

def create_message(*, text: str, role: Role = Role.user) -> Message:
    return Message(
        kind="message",
        role=role,
        parts=[Part(TextPart(kind="text", text=text))],
        message_id=uuid4().hex,
    )

async def main():
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as httpx_client:
        # 1) Discover agent card
        resolver = A2ACardResolver(httpx_client=httpx_client, base_url=PLANNER_BASE_URL)
        agent_card = await resolver.get_agent_card()

        # 2) Create client via factory (recommended)
        config = ClientConfig(httpx_client=httpx_client, streaming=False)
        client = ClientFactory(config).create(agent_card)

        # 3) Send message
        msg = create_message(text="Create a 5-step plan to launch a small internal hackathon at a fintech.")
        async for event in client.send_message(msg):
            # With streaming=False, you'll typically get one response
            if isinstance(event, Message):
                # Extract returned text
                out = ""
                for part in event.parts:
                    if hasattr(part, "text"):
                        out += part.text
                print(out)
                return
            else:
                # Sometimes you may get Task tuples etc.
                print(event)
                return

asyncio.run(main())
