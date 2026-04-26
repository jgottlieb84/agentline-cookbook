"""AI calls a patient to confirm an appointment.

The AI speaks first with a warm greeting, asks for confirmation, and
handles "yes", "no, please reschedule", and unclear responses.
Blocks until the call ends, then prints the transcript and summary.

    pip install agentline
    export AGENTLINE_API_KEY=ag_live_...
    python voice_appointment_confirm.py
"""

import os
from agentline import Agentline

client = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])

# Use a number you've already provisioned. If you don't have one:
#   number = client.provision_number(area_code="415")
#   from_ = number.phone_number
FROM_NUMBER = os.environ.get("FROM_NUMBER", "+14155551234")
PATIENT_NUMBER = os.environ.get("PATIENT_NUMBER", "+14155559999")

prompt = """
You are Sarah, a friendly appointment coordinator at Dr. Reyes's office.
Your job: confirm Maria's appointment for 2:00 PM this Thursday, April 24th.

If they say YES, thank them, wish them a good day, and end the call.
If they say NO or want to reschedule, apologize, offer to reschedule
(suggest the following Tuesday at 10 AM as an option), and tell them
someone from the front desk will call them back to finalize.
Keep it under 90 seconds. Be warm but efficient.
"""

result = client.make_call(
    from_=FROM_NUMBER,
    to=PATIENT_NUMBER,
    prompt=prompt,
    first_message="Hi, this is Sarah from Dr. Reyes's office. Is this Maria?",
    max_duration_seconds=120,
)

print(f"Call {result.id} — status: {result.status}")
print(f"Duration: {result.duration_seconds}s")
print(f"\nSummary: {result.summary}")
print("\nTranscript:")
for turn in result.transcript or []:
    print(f"  {turn.get('role')}: {turn.get('content')}")
