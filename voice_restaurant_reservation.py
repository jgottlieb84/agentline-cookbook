"""AI calls a restaurant and books a table.

Restaurants frequently require a phone call (their online reservation
systems don't cover all time slots). This recipe books a table for a
specified party size and target time, with two backup options.

    pip install agentline
    export AGENTLINE_API_KEY=ag_live_...
    python voice_restaurant_reservation.py
"""

import os
from agentline import Agentline

client = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])

FROM_NUMBER = os.environ.get("FROM_NUMBER", "+14155551234")
RESTAURANT_NUMBER = os.environ.get("RESTAURANT_NUMBER", "+14155554050")

prompt = """
You are calling a restaurant on behalf of Sam Rivera to book a table.

Details:
  • Party size: 4 people
  • Preferred time: Saturday, April 26th, 7:30 PM
  • Backup times (in order of preference): 7:00 PM same day, 8:00 PM same day, then Sunday same time
  • Name for the reservation: Sam Rivera
  • Callback number: the number you're calling FROM
  • No special dietary restrictions
  • It's a birthday dinner — mention it casually, in case they do anything special

Be warm and quick. If none of the times work, politely thank them and
hang up; you'll try another restaurant.

At the end, in your summary, output one line:
RESULT: BOOKED <time> | NO_AVAILABILITY | UNCLEAR
"""

result = client.make_call(
    from_=FROM_NUMBER,
    to=RESTAURANT_NUMBER,
    prompt=prompt,
    first_message="Hi, I'd like to make a reservation — do you have availability this Saturday night?",
    max_duration_seconds=180,
)

print(f"Status: {result.status}")
print(f"\n{result.summary}")
