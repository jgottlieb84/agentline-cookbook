"""AI calls another doctor's office to request medical records transfer.

A real use case: your office needs records from the patient's previous
provider. Rather than spending a staff member's afternoon on hold, an
AI agent makes the call.

    pip install agentline
    export AGENTLINE_API_KEY=ag_live_...
    python voice_medical_records.py
"""

import os
from agentline import Agentline

client = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])

FROM_NUMBER = os.environ.get("FROM_NUMBER", "+14155551234")
OTHER_OFFICE = os.environ.get("OTHER_OFFICE_NUMBER", "+14155552000")

prompt = """
You are calling ON BEHALF of Dr. Mei Chen's office to request medical
records transfer for a new patient.

Patient details:
  • Name: James Patterson
  • DOB: 1984-07-12
  • Last seen at your office: October 2024
  • Consent-to-release form has been signed and is on file at Dr. Chen's office
  • We can fax to (415) 555-3000 or send via secure email to records@drchen.example

Be polite and patient. Expect to be transferred once or put on hold.
If they need a signed release, offer to fax it; their fax number is the
one you want to confirm.

If they say the fastest path is to email a release form, get the correct
email address to send it to.

End the call by confirming the method of transfer and the approximate
timeline ("within 3 business days" etc). Max 6 minutes.
"""

result = client.make_call(
    from_=FROM_NUMBER,
    to=OTHER_OFFICE,
    prompt=prompt,
    first_message="Hi, I'm calling from Dr. Mei Chen's office. I need to request records transfer for a patient. Who's the best person to speak with about that?",
    max_duration_seconds=360,
)

print(f"Status: {result.status}")
print(f"\nSummary:\n{result.summary}")
