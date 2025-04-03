from .chain_of_thought import get_service_router_context
from .code_generation import system_instruction_prompt as sip_code_generation
from .classification import system_instruction_prompt as sip_classification
from .emotional_intelligence import system_instruction_prompt_linkedin as sip_emotional_intelligence_linkedin
from .few_shot_learning import get_extract_time_context
from .intent_recognition import system_instruction_prompt as sip_intent_recognition
from .rag_enabled_agents import system_instruction_prompt as sip_rag_enabled_agents, retrieve_top_k
from .function_calling import handle_query
from .groq import fetch_json