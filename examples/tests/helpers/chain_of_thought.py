import sys
import os

# Add the parent directory to sys.path so we can add examples/utils.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


system_instruction_prompt = """
You are an AI assistant designed to determine the correct service intent for routing a user's query. Follow a step-by-step approach based on the sequence of prior intents and the user's current input.

## Your Task:
1. You will be provided with a sequence of previously identified service intents.
2. You will also be provided with the user's current query.
3. Your task is to analyze both pieces of information and determine the most appropriate next service intent.

# Service Intent Definitions:
- check_account_balance: Retrieve the user's account balance.
- transfer_money: Transfer funds between accounts.
- check_transaction_status: Check the status of a past transaction.
- search_nearby_restaurants: Find nearby restaurants.
- view_restaurant_reviews: Retrieve reviews for a restaurant.
- book_table: Make a reservation at a restaurant.
- search_flights: Look up available flights.
- select_flight: Choose a flight.
- enter_passenger_details: Provide passenger information for a flight.
- retrieve_flight_information: Get details about a flight.
- search_product: Find a product.
- add_to_cart: Add a product to the shopping cart.
- apply_discount: Apply a discount code to the cart.

# Output Format (XML):
You will respond in a valid XML format with the <parts>, <reasoning>, and <intent> tags following below output format. You don't need to provide explanation or any other information, just return reasoning and intent.
- Reasoning: A short explanation of why this intent was chosen.
- Intent: The determined service intent.

# Format of the Output
<parts>
    <reasoning>The reasoning behind selecting this intent</reasoning>
    <intent>determined_service</intent>
</parts>

"""

example_previous_intents_1 = "check_account_balance -> transfer_money"
example_previous_user_query_1 = "Can you confirm if the transfer was successful?"
example_output_1 = """
    <parts>
        <reasoning>Can you confirm if the transfer was successful?"
        example_reasoning_1 = "The user has already requested to transfer funds. Now, they are asking about the status of that transfer. This query is related to checking the transaction status.</reasoning>
        <intent>check_transaction_status</intent>
    </parts>
"""

example_previous_intents_2 = "search_nearby_restaurants -> view_restaurant_reviews"
example_previous_user_query_2 = "Can you book a table for 7 PM?"
example_output_2 = """
    <parts>
        <reasoning>The user started by searching for restaurants and then viewed reviews. Now, they are asking to reserve a table at one of the restaurants. This query is related to making a reservation.</reasoning>
        <intent>book_table</intent>
    </parts>
"""

example_previous_intents_3 = "search_flights -> select_flight -> enter_passenger_details"
example_previous_user_query_3 = "What are the baggage policies for this airline?"
example_output_3 = """
    <parts>
        <reasoning>What are the baggage policies for this airline?"
        example_reasoning_3 = "The user has already selected a flight and entered passenger details. Now, they are asking for additional information about the flight's baggage policy. This query is related to retrieving flight details.</reasoning>
        <intent>retrieve_flight_information</intent>
    </parts>
"""

example_previous_intents_4 = "search_product -> add_to_cart"
example_previous_user_query_4 = "Can you apply a discount code for me?"
example_output_4 = """
    <parts>
        <reasoning>The user has added a product to their cart and now wants to apply a discount. This query is related to applying a coupon or promotion.</reasoning>
        <intent>apply_discount</intent>
    </parts>
"""


def get_service_router_context(previous_intents: str, service_request: str, legacy_api: bool = True) -> list:
    """
    Returns the context for the service router.
    """

    if legacy_api:
        context = [
            {"type": "Instruction", "text": system_instruction_prompt},

            {"type": "Human", "text": example_previous_intents_1},
            {"type": "Human", "text": example_previous_user_query_1},
            {"type": "AI", "text": example_output_1},

            {"type": "Human", "text": example_previous_intents_2},
            {"type": "Human", "text": example_previous_user_query_2},
            {"type": "AI", "text": example_output_2},

            {"type": "Human", "text": example_previous_intents_3},
            {"type": "Human", "text": example_previous_user_query_3},
            {"type": "AI", "text": example_output_3},

            {"type": "Human", "text": example_previous_intents_4},
            {"type": "Human", "text": example_previous_user_query_4},
            {"type": "AI", "text": example_output_4},
            {
                "type": "Human",
                "text": f"Query: {previous_intents}",
            },
            {
                "type": "Human",
                "text": f"Query: {service_request}",
            },
        ]
    else:
        context = [
                {"role": "system", "content": system_instruction_prompt},

                {"role": "user", "content": example_previous_intents_1},
                {"role": "user", "content": example_previous_user_query_1},
                {"role": "assistant", "content": example_output_1},

                {"role": "user", "content": example_previous_intents_2},
                {"role": "user", "content": example_previous_user_query_2},
                {"role": "assistant", "content": example_output_2},

                {"role": "user", "content": example_previous_intents_3},
                {"role": "user", "content": example_previous_user_query_3},
                {"role": "assistant", "content": example_output_3},

                {"role": "user", "content": example_previous_intents_4},
                {"role": "user", "content": example_previous_user_query_4},
                {"role": "assistant", "content": example_output_4},
                {
                    "role": "user",
                    "content": f"Query: {previous_intents}",
                },
                {
                    "role": "user",
                    "content": f"Query: {service_request}",
                },
            ]
    return context
