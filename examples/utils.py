import re
from typing import Dict
from inference import fetch as fetch_inflection

def parse_xml_response(xml_string: str, keys_to_search: list) -> Dict[str, object]:
    result = {}
    for k in keys_to_search:
        matches = re.search(rf"<{k}>(.+?)</{k}>", xml_string)
        value = matches.group(1) if matches is not None else ""
        if k == "participants":
            value = [participant.strip() for participant in value.strip('[]').split(',')]
        result[k] = value
    return result

async def get_response(
        context, 
        keys, 
        model="inflection_3_productivity",
        temperature: float = 0.0,
        top_p: float = 1,
        web_search: bool = False,
        legacy_api: bool = True
        ) -> Dict[str, object]:
    result = await fetch_inflection(
        context, 
        model,
        temperature,
        top_p,
        web_search,
        legacy_api
        )
    return parse_xml_response(result, keys)

def get_context(system_prompt: str, user_message: str, user_input_label: str = "User's input", legacy_api: bool = True) -> list:
    if legacy_api:
        context = [
            {"type": "Instruction", 
             "text": system_prompt
             },
            {
                "type": "Human",
                "text": f"{user_input_label}: {user_message}",
                },
        ]
        return context
    else: #OpenAI API
        context = [
            {"role": "system", 
             "content": system_prompt
            },
            {
            "role": "user",
            "content": f"{user_input_label}: {user_message}",
            },
        ]
    return context