import asyncio
import logging
from uuid import uuid4

import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import MessageSendParams, SendMessageRequest

logging.basicConfig(level=logging.INFO)

PLANNER_URL = "http://127.0.0.1:9000"
DEFAULT_TIMEOUT = 300


async def main():
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as http:
        resolver = A2ACardResolver(http_client=http)
        card = await resolver.resolve(PLANNER_URL)

        client = A2AClient(http_client=http, card=card)
        thread_id = str(uuid4())

        req = SendMessageRequest(
            params=MessageSendParams(
                thread_id=thread_id,
                message={
                    "role": "user",
                    "content": "Create a 5-step plan to launch a small internal hackathon at a fintech. Keep it practical.",
                },
            )
        )

        resp = await client.send_message(req)
        print(resp)


asyncio.run(main())
