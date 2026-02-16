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
        # TODO: 1) Discover the agent card using A2ACardResolver
        # Hint: resolver = A2ACardResolver(httpx_client=httpx_client, base_url=PLANNER_BASE_URL)
        #       agent_card = await resolver.get_agent_card()

        # TODO: 2) Create a client via ClientFactory
        # Hint: config = ClientConfig(httpx_client=httpx_client, streaming=False)
        #       client = ClientFactory(config).create(agent_card)

        # TODO: 3) Send a message and print the response
        # Hint: Create a message with create_message(text="...")
        #       Iterate over client.send_message(msg) using `async for`
        #       Check if event is a Message instance and extract text from event.parts
        pass

asyncio.run(main())
