# Description: This script demonstrates how to use the Inflection AI API to generate text completions based on a given context.
import os
import time
import aiohttp
import logging
from typing import List, Dict, Optional
from dotenv import load_dotenv

# load .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set your Inflection API key in your environment variables
base_url = os.getenv("BASE_URL")
inflection_api_key = os.getenv("INFLECTION_API_KEY")

async def fetch(
        context: List[Dict[str, str]], 
        model: str = "inflection_3_pi",
        temperature: float = 0.0,
        top_p: float = 1,
        web_search: bool = False,
        legacy_api: bool = True
        ) -> Optional[str]:                                 
    """
    Fetches a response from the Inflection AI API based on the provided context and model.

    Args:
        context: The context for the API request.
        model: The model configuration to use for the API request. The default is "inflection_3_pi". The available models are: "inflection_3_pi" and "inflection_3_productivity".
        legacy_api: A boolean flag to determine whether to use the legacy API or the OpenAI API. The default is True.

    Returns:
        Optional: The text response from the API, or None if an error occurs.
    """
    
    headers = {
        "Authorization": f"Bearer {inflection_api_key}",
        "Content-Type": "application/json",
    }

    if legacy_api:
        url = base_url + "/external/api/inference"

        json_payload = {
            "config": model, 
            "context": context,
            "temperature": temperature,
            "top_p": top_p,
            "web_search": web_search,
            }
    else:
        url = base_url + "/external/api/inference/openai/v1/chat/completions"

        json_payload = {
            "model": model, 
            "messages": context,
            "temperature": temperature,
            "top_p": top_p,
            "web_search": web_search,
            }

    logger.info(f"Sending messages to Inflection AI model '{model}'...")

    try:
        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            async with session.post(
                url, headers=headers, json=json_payload
            ) as response:
                response.raise_for_status()
                chat_completion = await response.json()
                end_time = time.time()
                duration = (end_time - start_time) * 1000  # Convert to milliseconds
                logger.info(f"Inflection AI API request took {duration:.2f} ms (Model=[{model}]) ")

                if not chat_completion:
                    logger.error("Invalid response format: 'text' field missing or empty")

                if legacy_api:
                    return chat_completion.get("text", None)
                else:
                    return chat_completion.get("choices")[0].get("message").get("content", None)
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return None