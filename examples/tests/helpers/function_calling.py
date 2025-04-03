import requests
import sys
import os

# Add the parent directory to sys.path so we can add examples/utils.py & examples/inference.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import get_context, get_response
from inference import fetch as fetch_inflection

system_instruction_prompt_intent = """
You are a helpful AI assistant designed to determine the intent of a user's query.

# Your Purpose
1. Identify the intent behind the user's message.
2. Do not attempt to answer or solve the user's query.
3. Only classify the query into one of the valid intents listed below.
4. Do not invent new intents—select only from the predefined list.
5. Always review the valid intents before making a selection.

# Valid Intents
- weather: The user is asking about the weather.
- other: The user's query does not pertain to the weather.

# Output Format - XML
You will respond using XML tags for each extracted piece of information. You don't need to provide explanation or any other information, just return the extracted parts within the appropriate XML tags.

# Format of the Output
<parts>
    <reasoning>The reasoning behind selecting this intent</reasoning>
    <intent_recognized>intent_selected</intent_recognized>
</parts>
"""

system_instruction_prompt_lat_long = """
You are a helpful AI assistant designed to extract the latitude and longitude of a location mentioned in the user's query.

# Your Purpose
1. Identify and return the latitude and longitude of the location specified by the user.
2. Provide only numerical values for latitude and longitude no degree symbols (°) or directional indicators (N, S, E, W).
3. Do NOT attempt to answer or interpret the user's query beyond extracting coordinates.

# Output Format - XML
You will respond using XML tags for each extracted piece of information. You don't need to provide explanation or any other information, just return the extracted parts within the appropriate XML tags.

# Format of the Output
<parts>
    <latitude>Extracted latitude</latitude>
    <longitude>Extracted longitude</longitude>
</parts>
"""

system_instruction_prompt_weather = """
You are a helpful AI assistant designed to generate friendly weather responses based on provided weather data and the user's original message.

# Your Purpose
1. Construct a response using the provided weather information: (temperature in Celsius and Fahrenheit) and the user's original message.
2. Make the response engaging and friendly, using appropriate emojis.
3. Do NOT add any extra information, only reformat the given weather data and message into a natural response.
4. Ensure clarity, warmth, and helpfulness in your wording.

# Additional Instructions
1. DO NOT provide any details beyond the given weather data and original message.
2. DO NOT attempt to answer or interpret the user's query beyond constructing the weather response.

Example Input: 
Original Message: What is the weather in NYC?
Current temperature: 1°C (33.2°F)

Example Output: The current temperature in NYC is 1°C (33.2°F). Stay warm!
"""

system_instruction_prompt_general = """
You are a helpful AI assistant designed to assist users with their queries in a polite and informative manner.

# Your Purpose
1. Provide helpful, accurate, and well-structured responses to user questions.
2. Maintain a polite, friendly, and professional tone in all interactions.
3. Answer questions to the best of your ability, ensuring clarity and relevance.
4. Be concise yet informative, avoid unnecessary details or overly complex explanations.
5. Maintain a friendly and approachable tone to enhance user experience.
6. Adapt your response style based on the user's query to ensure clarity and helpfulness.
"""


def get_weather(latitude: str, longitude: str) -> dict:
    """
    Get the weather information for the given latitude and longitude.
    """
    # Fetch the weather data in Celsius
    response_celsius = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m&temperature_unit=celsius")
    data_celsius = response_celsius.json()
    temperature_celsius = data_celsius['current']['temperature_2m']

    # Fetch the weather data in Fahrenheit
    response_fahrenheit = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m&temperature_unit=fahrenheit")
    data_fahrenheit = response_fahrenheit.json()
    temperature_fahrenheit = data_fahrenheit['current']['temperature_2m']

    # Return both temperatures
    return {
        'temperature_celsius': temperature_celsius,
        'temperature_fahrenheit': temperature_fahrenheit
    }


async def handle_query(query: str, legacy_api: bool=True) -> str:
    
    # Extract the intent
    context = get_context(system_instruction_prompt_intent, query, legacy_api=legacy_api)
    result = await get_response(context, ["reasoning", "intent_recognized"], legacy_api=legacy_api)
    intent = result["intent_recognized"]

    match intent:
        case "weather":
            context_2 = get_context(system_instruction_prompt_lat_long, query, legacy_api=legacy_api)
            result = await get_response(context_2, ["latitude", "longitude"], legacy_api=legacy_api)
            lat = result["latitude"]
            long = result["longitude"]
            weather = get_weather(lat, long)
            message = f""" 
            Original Message: {query}
            Current temperature: {weather['temperature_celsius']}°C ({weather['temperature_fahrenheit']}°F)"""
            context_3 = get_context(system_instruction_prompt_weather, message, legacy_api=legacy_api)
            return await fetch_inflection(context_3, legacy_api=legacy_api)
        case "other":
            context_2 = get_context(system_instruction_prompt_general, query, legacy_api=legacy_api)
            return await fetch_inflection(context_2, legacy_api=legacy_api)
