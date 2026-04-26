"""Capture an SMS 2FA code during signup.

The killer Agentline flow: provision a fresh phone number, paste it into
a signup form, wait for the verification SMS, extract the code.

    pip install agentline
    export AGENTLINE_API_KEY=ag_live_...
    python sms_2fa_signup.py
"""

import os
from agentline import Agentline

client = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])

phone, code = client.capture_code(area_code="415", timeout=120)

print(f"Use this phone number in the signup form: {phone}")
print(f"2FA code received: {code}")
