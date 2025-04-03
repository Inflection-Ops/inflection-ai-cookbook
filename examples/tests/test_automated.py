import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from artifacts import linkedin_notifications_artifact_content
from .helpers import (
    get_service_router_context,
    sip_code_generation,
    sip_classification,
    sip_emotional_intelligence_linkedin,
    sip_intent_recognition,
    sip_rag_enabled_agents,
    get_extract_time_context,
    retrieve_top_k,
    handle_query,
    fetch_json
)

from utils import get_context, get_response
from inference import fetch as fetch_inflection
from typing import Any, Dict, Optional

pytestmark = pytest.mark.asyncio

code_generation_validation_system_prompt = """
You are a code reviewer responsible for validating generated code. Analyze the code based on:
1. Correctness: Does the code solve the given problem?
2. Syntax: Is the code syntactically correct?
3. Best practices: Does it follow Python coding standards?

Return a JSON response with the following structure:
{
    "is_valid": boolean,
    "reasoning": string,
    "suggestions": list[string] (if any improvements needed)
}
"""

async def validate_generated_code(instructions: str, generated_code: str) -> Optional[Dict[str, Any]]:
    validation_prompt = f"""
    Original Instructions:
    {instructions}

    Generated Code:
    {generated_code}

    Please validate if this code correctly implements the requirements.
    """

    return await fetch_json(code_generation_validation_system_prompt, validation_prompt)


@pytest.mark.asyncio
@pytest.mark.parametrize("legacy_api", [True, False])
async def test_code_generation_and_validation(legacy_api: bool):
    """Test the complete flow of code generation and validation."""
    print(f"Starting test: test_code_generation_and_validation with legacy_api={legacy_api}")
    print("-" * 50)

    # Test case 1: Simple function generation
    instructions = """
    Write a Python function to return the sum of two numbers.
    """

    # Get the code generation context
    context = get_context(
        sip_code_generation,
        instructions,
        user_input_label="User's instructions:",
        legacy_api=legacy_api
    )

    # Generate code using Inflection
    generated_code = await fetch_inflection(context, legacy_api=legacy_api)
    assert generated_code is not None, "Code generation failed"
    print(f"Generated Code:\n{generated_code}\n")

    # Validate the generated code using Groq
    validation_result = await validate_generated_code(instructions, generated_code)
    assert validation_result is not None, "Code validation failed"
    print(f"Validation Result:\n{validation_result}\n")

    # Assert validation results
    assert "is_valid" in validation_result, "Missing 'is_valid' in validation response"
    assert isinstance(validation_result["is_valid"], bool), "'is_valid' should be boolean"
    assert "reasoning" in validation_result, "Missing 'reasoning' in validation response"

    # Log validation results
    if validation_result["is_valid"]:
        print(f"✅ Code generation test passed with legacy_api={legacy_api}!")
        if "suggestions" in validation_result and validation_result["suggestions"]:
            print("Suggestions for improvement:")
            for suggestion in validation_result["suggestions"]:
                print(f"- {suggestion}")
    else:
        print(f"❌ Code generation test failed with legacy_api={legacy_api}!")
        print(f"Reason: {validation_result['reasoning']}")
        if "suggestions" in validation_result:
            print("Suggestions for fixes:")
            for suggestion in validation_result["suggestions"]:
                print(f"- {suggestion}")

    return validation_result

@pytest.mark.asyncio
@pytest.mark.parametrize("legacy_api", [True, False])
async def test_restaurant_review_flow(legacy_api: bool):
    """Test the natural flow from restaurant search to viewing reviews"""
    previous_intents = "search_nearby_restaurants"
    service_request = "Please show me the reviews."
    context = get_service_router_context(previous_intents, service_request, legacy_api=legacy_api)
    result = await get_response(context, ["reasoning", "intent"], legacy_api=legacy_api)

    assert result["intent"] == "view_restaurant_reviews"


@pytest.mark.asyncio
@pytest.mark.parametrize("legacy_api", [True, False])
async def test_document_classification(legacy_api: bool):
    document_text = """
    Project Alpha

    Scope and Objectives:Develop a customer management platform for small businesses with user-friendly interfaces.

    Deliverables:

        - Functional web application.

        - Deployment documentation.

    Milestones:

        - Prototype by March 15, 2025.

        - Final delivery by May 30, 2025.

    Payment Terms:

        --50% upfront.

        - 50% on final delivery.

    Responsibilities:

        Client: Provide requirements and feedback.

        Contractor: Deliver on time and as specified.
    """
    context = get_context(sip_classification, document_text, legacy_api=legacy_api)
    result = await get_response(context, ["category"], legacy_api=legacy_api)
    assert result["category"] == "statement_of_work"
    print(f"Category: {result["category"]}")


@pytest.mark.asyncio
@pytest.mark.parametrize("legacy_api", [True, False])
async def test_emotional_intelligence(legacy_api: bool):
    message = linkedin_notifications_artifact_content + "\n # Which Notification Or Message The Human Wants You To Draft A Reply To: New Connection Request: John Smith"
    context = get_context(sip_emotional_intelligence_linkedin, message, legacy_api=legacy_api)
    result = await get_response(context, ["response"], legacy_api=legacy_api)

    system_prompt = """
You are a personal assistant who have been tasked to review an AI generated outgoing message. Evaluate the given message based on correctness, clarity, professionalism, relevance, politeness, and security.

Return a JSON response with the following structure:
{
    "is_valid": boolean,
    "reasoning": string,
    "suggestions": list[string] (if any improvements needed)
}
"""

    validation_prompt = f"""
    Original Instructions:
    {message}

    Generated message:
    {result['response']}

    Please validate if generated message correctly implements the original instructions.
    """

    validation_result = await fetch_json(system_prompt, validation_prompt)

    assert validation_result is not None, "Message validation failed"

    print(f"Validation Result:\n{validation_result}\n")

    # Assert validation results
    assert "is_valid" in validation_result, "Missing 'is_valid' in validation response"
    assert isinstance(validation_result["is_valid"], bool), "'is_valid' should be boolean"
    assert "reasoning" in validation_result, "Missing 'reasoning' in validation response"


@pytest.mark.asyncio
@pytest.mark.parametrize("legacy_api", [True, False])
async def test_few_shot_learning(legacy_api: bool):
    message = "Let's schedule the meeting for 5pm for 2 hours"
    context = get_extract_time_context(message, legacy_api=legacy_api)
    result = await get_response(context, ["start_time", "end_time"], legacy_api=legacy_api)
    print(result)

    system_prompt = '''
Evaluate the JSON output from GPT to ensure the start and end time of the meeting match the requested schedule. Check for correctness, logical consistency, and time conflicts. 

Return a JSON response with the following structure:
{
    "is_valid": boolean,
    "reasoning": string
}
'''

    validation_prompt = f"""
    Original Instructions:
    {message}

    Generated message:
    {result}
    """

    validation_result = await fetch_json(system_prompt, validation_prompt)

    assert validation_result is not None, "Message validation failed"

    print(f"Validation Result:\n{validation_result}\n")

    # Assert validation results
    assert "is_valid" in validation_result, "Missing 'is_valid' in validation response"
    assert isinstance(validation_result["is_valid"], bool), "'is_valid' should be boolean"
    assert "reasoning" in validation_result, "Missing 'reasoning' in validation response"


@pytest.mark.asyncio
@pytest.mark.parametrize("legacy_api", [True, False])
async def test_function_calling(legacy_api: bool):
    message = "What is the weather in Hawaii?"
    result = await handle_query(message, legacy_api=legacy_api)
    print(result)

    system_prompt = '''
Evaluate the output from GPT to ensure the it matches the intent and desired output of the original instructions. Check for correctness, logical consistency and proper sentence structure. 

Return a JSON response with the following structure:
{
    "is_valid": boolean,
    "reasoning": string
}
'''

    validation_prompt = f"""
    Original Instructions:
    {message}

    Generated message:
    {result}
    """

    validation_result = await fetch_json(system_prompt, validation_prompt)

    assert validation_result is not None, "Message validation failed"

    print(f"Validation Result:\n{validation_result}\n")

    # Assert validation results
    assert "is_valid" in validation_result, "Missing 'is_valid' in validation response"
    assert isinstance(validation_result["is_valid"], bool), "'is_valid' should be boolean"
    assert "reasoning" in validation_result, "Missing 'reasoning' in validation response"


@pytest.mark.asyncio
@pytest.mark.parametrize("legacy_api", [True, False])
async def test_intent_recognition(legacy_api: bool):
    system_prompt = '''
    Evaluate the recognized intent from GPT to ensure that it matches the original email message passed in to it. Make sure that the recognized intent is logically correct and closed relates to the intent of the original message. 

    Return a JSON response with the following structure:
    {
        "is_valid": boolean,
        "reasoning": string
    }
    '''

    email_body = "Good day! I stumbled upon a charming little bug in one of your functions, please fix."
    context = get_context(sip_intent_recognition, email_body, user_input_label="Email body", legacy_api=legacy_api)
    result = await get_response(context, ["reasoning", "intent_recognized"], legacy_api=legacy_api)

    validation_prompt = f"""
    Original email message:
    {email_body}

    Recognized intent:
    {result["intent_recognized"]}
    """

    validation_result = await fetch_json(system_prompt, validation_prompt)

    assert validation_result is not None, "Message validation failed"
    print(f"Validation Result:\n{validation_result}\n")

    # Assert validation results
    assert "is_valid" in validation_result, "Missing 'is_valid' in validation response"
    assert isinstance(validation_result["is_valid"], bool), "'is_valid' should be boolean"
    assert "reasoning" in validation_result, "Missing 'reasoning' in validation response"

    email_body = "Do you have time to meet today to strategize our next masterstroke, or shall we let the universe think it's gotten the upper hand?"
    context = get_context(sip_intent_recognition, email_body, user_input_label="Email body", legacy_api=legacy_api)
    result = await get_response(context, ["reasoning", "intent_recognized"], legacy_api=legacy_api)

    validation_prompt = f"""
    Original email message:
    {email_body}

    Recognized intent:
    {result["intent_recognized"]}
    """

    validation_result = await fetch_json(system_prompt, validation_prompt)

    assert validation_result is not None, "Message validation failed"
    print(f"Validation Result:\n{validation_result}\n")

    # Assert validation results
    assert "is_valid" in validation_result, "Missing 'is_valid' in validation response"
    assert isinstance(validation_result["is_valid"], bool), "'is_valid' should be boolean"
    assert "reasoning" in validation_result, "Missing 'reasoning' in validation response"


@pytest.mark.asyncio
@pytest.mark.parametrize("legacy_api", [True, False])
async def test_rag_enabled_agents(legacy_api: bool):
    question = "What are the benefits of electric vehicles?"
    retrieved_chunks = retrieve_top_k(question)

    query = f"Query: {question}\nRetrieved context: {retrieved_chunks}"
    context = get_context(sip_rag_enabled_agents, query, legacy_api=legacy_api)
    result = await fetch_inflection(context, legacy_api=legacy_api)
    print(result)

    system_prompt = '''
Evaluate the RAG output from GPT to ensure that the retrieved chunks are relevant to the question itself and the final response is logically correct and answers the original question that was asked and provides more relevant augmented response. 

Return a JSON response with the following structure:
{
    "is_valid": boolean,
    "reasoning": string
}
'''

    validation_prompt = f"""
    Original Question:
    {question}

    Retrieved Chunks:
    {retrieved_chunks}

    Generated response:
    {result}
    """

    validation_result = await fetch_json(system_prompt, validation_prompt)

    assert validation_result is not None, "Message validation failed"

    print(f"Validation Result:\n{validation_result}\n")

    # Assert validation results
    assert "is_valid" in validation_result, "Missing 'is_valid' in validation response"
    assert isinstance(validation_result["is_valid"], bool), "'is_valid' should be boolean"
    assert "reasoning" in validation_result, "Missing 'reasoning' in validation response"


if __name__ == "__main__":
    pytest.main(["-v"])
