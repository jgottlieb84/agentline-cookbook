"""AI calls each person on a list and asks a 3-question survey.

Each call is blocking (simple for a cookbook); in production you'd place
calls in parallel with `wait=False` and poll for completion.

    pip install agentline
    export AGENTLINE_API_KEY=ag_live_...
    python voice_survey.py
"""

import os
from agentline import Agentline

client = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])

FROM_NUMBER = os.environ.get("FROM_NUMBER", "+14155551234")

RESPONDENTS = [
    "+14155551001",
    "+14155551002",
    "+14155551003",
]

prompt = """
You are Jordan, a customer research assistant.
Ask exactly these three questions in order, one at a time:
  1. How likely are you to recommend our product to a friend, on a scale of 0 to 10?
  2. What's the single biggest reason for that score?
  3. What's one thing we could change that would move your score up by 2?

Be warm, listen to answers, don't argue or try to sell anything. Thank them at the end.
Max 3 minutes total.

At the end, in the summary, output three lines:
NPS: <number>
REASON: <one sentence>
SUGGESTION: <one sentence>
"""

for phone in RESPONDENTS:
    print(f"\nCalling {phone}...")
    result = client.make_call(
        from_=FROM_NUMBER,
        to=phone,
        prompt=prompt,
        first_message="Hi, this is Jordan. Do you have two minutes for three quick questions about your recent experience with our product?",
        max_duration_seconds=240,
    )
    print(f"  {result.status}: {result.summary}")
