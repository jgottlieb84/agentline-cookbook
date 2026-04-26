"""Capture an email-based verification code during signup.

Provision a disposable email address, paste into the signup form, wait for
the verification email to arrive, extract the code, release the address.

    pip install agentline
    export AGENTLINE_API_KEY=ag_live_...
    python email_2fa_signup.py
"""

import os
from agentline import Agentline

client = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])

email, code = client.capture_email_code(timeout=180)

print(f"Use this email in the signup form: {email}")
print(f"Verification code received: {code}")
