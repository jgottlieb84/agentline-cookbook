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

def submit_signup(address: str) -> None:
    input(f"Enter {address} in your signup form, request a code, then press Enter here: ")

email, code = client.capture_email_code(timeout=120, on_provision=submit_signup)
print(f"Verification code: {code}")
