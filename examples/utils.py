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

async def get_response(context, keys, model="inflection_3_productivity") -> Dict[str, object]:
    result = await fetch_inflection(context, model)
    return parse_xml_response(result, keys)

def get_context(system_prompt: str, user_message: str, user_input_label: str = "User's input") -> list:
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