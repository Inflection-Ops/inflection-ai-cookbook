import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from .helpers import get_service_router_context
from utils import get_response


@pytest.mark.asyncio
@pytest.mark.parametrize("legacy_api", [True, False])
async def test_restaurant_review_flow(legacy_api: bool):
    """Test the natural flow from restaurant search to viewing reviews"""
    previous_intents = "search_nearby_restaurants"
    service_request = "Please show me the reviews."
    context = get_service_router_context(previous_intents, service_request, legacy_api=legacy_api)
    result = await get_response(context, ["reasoning", "intent"], legacy_api=legacy_api)

    assert result["intent"] == "view_restaurant_reviews"
    assert "reasoning" in result


@pytest.mark.asyncio
@pytest.mark.parametrize("legacy_api", [True, False])
async def test_no_previous_intent(legacy_api: bool):
    """Test behavior when there's no previous intent"""
    previous_intents = ""
    service_request = "Show me restaurant reviews"
    context = get_service_router_context(previous_intents, service_request, legacy_api=legacy_api)
    result = await get_response(context, ["reasoning", "intent"], legacy_api=legacy_api)

    assert result["intent"] == "view_restaurant_reviews"

@pytest.mark.asyncio
@pytest.mark.parametrize("legacy_api", [True, False])
async def test_ambiguous_request(legacy_api: bool):
    """Test handling of ambiguous review requests"""
    previous_intents = "search_nearby_restaurants"
    service_request = "What do people think about it?"
    context = get_service_router_context(previous_intents, service_request, legacy_api=legacy_api)
    result = await get_response(context, ["reasoning", "intent"], legacy_api=legacy_api)

    assert result["intent"] == "view_restaurant_reviews"
    assert "reasoning" in result

if __name__ == "__main__":
    pytest.main(["-v"])
