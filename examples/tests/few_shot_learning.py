system_instruction_prompt = """
You are an AI assistant designed to extract and format meeting time slots from user responses.

# Your Task
1. Given a user's response, identify the provided meeting time slot.
2. If the response includes both a start and end time, extract them directly.
3. If only a start time is given, calculate the end time based on the provided duration.

# Output Format - XML
You will respond in a valid XML format with the <parts>, <start_time>, and  <end_time> tags following the output format. You don't need to provide explanation or any other information, just return the extracted time slot.

# Format of the Output
<parts>
  <start_time>start_time_extracted</start_time>
  <end_time>end_time_extracted</end_time>
</parts>
"""

example_input_1 = "2:00-4:00pm is good for me"
example_output_1 = """
    <parts>
      <start_time>14:00</start_time>
      <end_time>16:00</end_time>
    </parts>
"""

example_input_2 = "Let's schedule the meeting for 10:00am. Duration: 30 minutes"
example_output_2 = """
    <parts>
      <start_time>10:00</start_time>
      <end_time>10:30</end_time>
    </parts>
"""


def get_extract_time_context(message: str) -> list:
    context = [
        {"type": "Instruction", "text": system_instruction_prompt},
        {"type": "Human", "text": example_input_1},
        {"type": "AI", "text": example_output_1},
        {"type": "Human", "text": example_input_2},
        {"type": "AI", "text": example_output_2},
        {
            "type": "Human",
            "text": f"Email body: {message}",
        },
    ]
    return context
