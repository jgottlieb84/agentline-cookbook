"""Provision an ephemeral identity: fresh phone + email, use both, release both.

For services that ask for BOTH a phone number AND an email during signup.
We block for the SMS code first, then the email code (many services send
both in sequence — SMS for 2FA, email for confirmation link).

    pip install agentline
    export AGENTLINE_API_KEY=ag_live_...
    python disposable_identity.py
"""

import os
from agentline import Agentline

client = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])

number = client.provision_number(area_code="415")
email = client.create_email_address()

print(f"Phone: {number.phone_number}")
print(f"Email: {email.email_address}")
print("Paste both into the signup form, then press Enter...")
input()

sms_code = client.get_verification_code(number.phone_number, timeout=120)
print(f"SMS code: {sms_code}")

email_code = client.get_email_verification_code(email.email_address, timeout=180)
print(f"Email code: {email_code}")

client.release_number(number.phone_number)
client.release_email_address(email.id)
print("Identity released.")
