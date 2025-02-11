import pytest
from examples.tests.chain_of_thought import get_service_router_context
from utils import get_response

@pytest.mark.asyncio
async def test_restaurant_review_flow():
    """Test the natural flow from restaurant search to viewing reviews"""
    previous_intents = "search_nearby_restaurants"
    service_request = "Please show me the reviews."
    context = get_service_router_context(previous_intents, service_request)
    result = await get_response(context, ["reasoning", "intent"])

    assert result["intent"] == "view_restaurant_reviews"
    assert "reasoning" in result


@pytest.mark.asyncio
async def test_no_previous_intent():
    """Test behavior when there's no previous intent"""
    previous_intents = ""
    service_request = "Show me restaurant reviews"
    context = get_service_router_context(previous_intents, service_request)
    result = await get_response(context, ["reasoning", "intent"])

    assert result["intent"] == "view_restaurant_reviews"

@pytest.mark.asyncio
async def test_ambiguous_request():
    """Test handling of ambiguous review requests"""
    previous_intents = "search_nearby_restaurants"
    service_request = "What do people think about it?"
    context = get_service_router_context(previous_intents, service_request)
    result = await get_response(context, ["reasoning", "intent"])

    assert result["intent"] == "view_restaurant_reviews"
    assert "reasoning" in result

if __name__ == "__main__":
    pytest.main(["-v"])
