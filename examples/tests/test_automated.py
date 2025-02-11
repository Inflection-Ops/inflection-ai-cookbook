import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from chain_of_thought import get_service_router_context
from artifacts import linkedin_notifications_artifact_content
from code_generation import system_instruction_prompt as sip_code_generation
from classification import system_instruction_prompt as sip_classification
from emotional_intelligence import system_instruction_prompt_linkedin as sip_emotional_intelligence_linkedin
from few_shot_learning import get_extract_time_context
from intent_recognition import system_instruction_prompt as sip_intent_recognition
from rag_enabled_agents import system_instruction_prompt as sip_rag_enabled_agents, retrieve_top_k
from function_calling import handle_query
from groq import fetch_json
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
async def test_restaurant_review_flow():
    """Test the natural flow from restaurant search to viewing reviews"""
    previous_intents = "search_nearby_restaurants"
    service_request = "Please show me the reviews."
    context = get_service_router_context(previous_intents, service_request)
    result = await get_response(context, ["reasoning", "intent"])

    assert result["intent"] == "view_restaurant_reviews"


@pytest.mark.asyncio
async def test_code_generation_and_validation():
    """Test the complete flow of code generation and validation."""
    print("Starting test: test_code_generation_and_validation")
    print("-" * 50)

    # Test case 1: Simple function generation
    instructions = """
    Write a Python function to return the sum of two numbers.
    """

    # Get the code generation context
    context = get_context(
        sip_code_generation,
        instructions,
        user_input_label="User's instructions:"
    )

    # Generate code using Inflection
    generated_code = await fetch_inflection(context)
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
        print("✅ Code generation test passed!")
        if "suggestions" in validation_result and validation_result["suggestions"]:
            print("Suggestions for improvement:")
            for suggestion in validation_result["suggestions"]:
                print(f"- {suggestion}")
    else:
        print("❌ Code generation test failed!")
        print(f"Reason: {validation_result['reasoning']}")
        if "suggestions" in validation_result:
            print("Suggestions for fixes:")
            for suggestion in validation_result["suggestions"]:
                print(f"- {suggestion}")

    return validation_result


@pytest.mark.asyncio
async def test_document_classification():
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
    context = get_context(sip_classification, document_text)
    result = await get_response(context, ["category"])
    assert result["category"] == "statement_of_work"
    print(f"Category: {result["category"]}")


@pytest.mark.asyncio
async def test_emotional_intelligence():
    message = linkedin_notifications_artifact_content + "\n # Which Notification Or Message The Human Wants You To Draft A Reply To: New Connection Request: John Smith"
    context = get_context(sip_emotional_intelligence_linkedin, message)
    result = await get_response(context, ["response"])

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
async def test_few_shot_learning():
    message = "Let's schedule the meeting for 5pm for 2 hours"
    context = get_extract_time_context(message)
    result = await get_response(context, ["start_time", "end_time"])
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
async def test_function_calling():
    message = "What is the weather in Hawaii?"
    result = await handle_query(message)
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
async def test_intent_recognition():
    system_prompt = '''
    Evaluate the recognized intent from GPT to ensure that it matches the original email message passed in to it. Make sure that the recognized intent is logically correct and closed relates to the intent of the original message. 

    Return a JSON response with the following structure:
    {
        "is_valid": boolean,
        "reasoning": string
    }
    '''

    email_body = "Good day! I stumbled upon a charming little bug in one of your functions, please fix."
    context = get_context(sip_intent_recognition, email_body, user_input_label="Email body")
    result = await get_response(context, ["reasoning", "intent_recognized"])

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
    context = get_context(sip_intent_recognition, email_body, user_input_label="Email body")
    result = await get_response(context, ["reasoning", "intent_recognized"])

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
async def test_rag_enabled_agents():
    question = "What are the benefits of electric vehicles?"
    retrieved_chunks = retrieve_top_k(question)

    query = f"Query: {question}\nRetrieved context: {retrieved_chunks}"
    context = get_context(sip_rag_enabled_agents, query)
    result = await fetch_inflection(context)
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
