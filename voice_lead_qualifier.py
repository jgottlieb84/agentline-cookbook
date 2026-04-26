"""AI calls a lead, runs through BANT qualification, returns a verdict.

BANT = Budget, Authority, Need, Timeline. The AI asks casually — not like
a script — and judges at the end whether this lead is qualified.

    pip install agentline
    export AGENTLINE_API_KEY=ag_live_...
    python voice_lead_qualifier.py
"""

import os
from agentline import Agentline

client = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])

FROM_NUMBER = os.environ.get("FROM_NUMBER", "+14155551234")
LEAD_NUMBER = os.environ.get("LEAD_NUMBER", "+14155557777")

prompt = """
You are Alex, a sales development rep at an AI infra company.
Call goal: qualify this inbound lead using BANT.

Ask naturally, not robotically:
  • Budget — do they have budget allocated for AI tooling this quarter?
  • Authority — are they the decision-maker, or who signs off?
  • Need — what problem are they trying to solve?
  • Timeline — when would they want to have this in production?

Keep it conversational. Max 4 minutes. At the end, thank them and say
someone will follow up via email with next steps.

At the very end of the call, in your summary, output a single line:
VERDICT: QUALIFIED | NOT_QUALIFIED | NEEDS_MORE_INFO
"""

result = client.make_call(
    from_=FROM_NUMBER,
    to=LEAD_NUMBER,
    prompt=prompt,
    first_message="Hey, this is Alex from Agentline. Got a minute to chat about the demo request you submitted?",
    max_duration_seconds=300,
)

print(f"Status: {result.status}  duration: {result.duration_seconds}s\n")
print("Summary:")
print(result.summary)
