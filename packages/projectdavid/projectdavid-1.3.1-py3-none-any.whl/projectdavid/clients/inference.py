import asyncio
import json
import time
from typing import AsyncGenerator, Optional

import httpx
from dotenv import load_dotenv
from projectdavid_common import UtilsInterface
from projectdavid_common.schemas.stream import StreamRequest
from pydantic import ValidationError

load_dotenv()

logging_utility = UtilsInterface.LoggingUtility()

DEFAULT_TIMEOUT = httpx.Timeout(30.0, connect=10.0, read=30.0, write=10.0, pool=30.0)


class InferenceClient:
    """
    Client-side service for interacting with the completions endpoint.

    Exposes:
      - create_completion_sync(...): a synchronous wrapper that blocks until the response is aggregated.
      - stream_inference_response(...): an async generator for real-time streaming.
    """

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: Optional[httpx.Timeout] = None,
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout or DEFAULT_TIMEOUT

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        self.client = httpx.Client(
            base_url=self.base_url, headers=headers, timeout=self.timeout
        )
        logging_utility.info(
            "InferenceClient initialized with base_url: %s", self.base_url
        )

    def create_completion_sync(
        self,
        provider: str,
        model: str,
        thread_id: str,
        message_id: str,
        run_id: str,
        assistant_id: str,
        user_content: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> dict:
        payload = {
            "provider": provider,
            "model": model,
            "api_key": api_key,
            "thread_id": thread_id,
            "message_id": message_id,
            "run_id": run_id,
            "assistant_id": assistant_id,
        }
        if user_content:
            payload["content"] = user_content

        try:
            request = StreamRequest(**payload)
        except ValidationError as e:
            logging_utility.error("Payload validation error: %s", e.json())
            raise ValueError(f"Payload validation error: {e}")

        logging_utility.info(
            "Sending completions request (sync wrapper): %s", request.dict()
        )

        async def aggregate() -> str:
            final_text = ""
            async for chunk in self.stream_inference_response(request):
                final_text += chunk.get("content", "")
            return final_text

        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            final_content = loop.run_until_complete(aggregate())
        finally:
            loop.close()

        return {
            "id": f"chatcmpl-{run_id}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request.mapped_model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": final_content},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": len(final_content.split()),
                "total_tokens": len(final_content.split()),
            },
        }

    async def stream_inference_response(
        self, request: StreamRequest
    ) -> AsyncGenerator[dict, None]:
        logging_utility.info("Sending streaming inference request: %s", request.dict())

        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

        async with httpx.AsyncClient(
            base_url=self.base_url, timeout=self.timeout, headers=headers
        ) as async_client:
            try:
                async with async_client.stream(
                    "POST", "/v1/completions", json=request.dict()
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line.startswith("data:"):
                            data_str = line[len("data:") :].strip()
                            if data_str == "[DONE]":
                                break
                            try:
                                yield json.loads(data_str)
                            except json.JSONDecodeError as json_exc:
                                logging_utility.error(
                                    "Error decoding JSON from stream: %s", str(json_exc)
                                )
            except httpx.HTTPStatusError as e:
                logging_utility.error(
                    "HTTP error during streaming completions: %s", str(e)
                )
                raise
            except Exception as e:
                logging_utility.error(
                    "Unexpected error during streaming completions: %s", str(e)
                )
                raise

    def close(self):
        self.client.close()
