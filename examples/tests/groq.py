import json
import logging
import time
from typing import Any, Dict, Optional

from openai import OpenAI, RateLimitError
from pydantic import BaseModel


class SidePanelContent(BaseModel):
    title: str
    thread_id: str | None
    markdown_content: str | None
    json_content: dict | None
    type: str


class Message(BaseModel):
    role: str
    content: str
    id: str
    artifact: SidePanelContent | None = None
    intent: str | None = None
    timestamp: str


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Initialize the OpenAI client with Groq's API Key
client = OpenAI(api_key="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",
                base_url="https://api.groq.com/openai/v1")


async def fetch_json(system_message: str, user_message: str) -> Optional[Dict[str, Any]]:
    """Fetches a JSON response from Groq API."""
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]

    logger.info(f"Sending messages to Groq API... {messages}")

    try:
        start_time = time.time()  # Record the start time
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-70b-8192",
            temperature=1e-8,  # As per Groq's requirement for handling temperature
            response_format={"type": "json_object"},  # Ensure correct parameter format
        )
        end_time = time.time()  # Record the end time
        duration = (end_time - start_time) * 1000  # Calculate duration in milliseconds
        logger.info(f"Groq API request took {duration:.2f} ms")
        json_string = chat_completion.choices[0].message.content  # Extract JSON string

        try:
            json_response = json.loads(
                json_string
            )
            logger.info(f"JSON response: {json_response}")

        except json.JSONDecodeError:
            logger.exception("Failed to decode JSON string.")
            return None
        else:
            return json_response

    except RateLimitError:
        logger.exception("Request exceeded rate limit")
        return None
    except Exception as e:
        logger.exception(f"Error calling Groq.{e}")
        return None
