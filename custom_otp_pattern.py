"""Capture OTPs that aren't standard 4-8 digit numbers.

Some services send alphanumeric codes (e.g. "A3F7-BK92"), 4-digit PINs, or
codes with prefixes ("Your code is: 123456"). Use `wait_for_sms(match=...)`
with a custom regex — the server holds the connection open until a message
matching the pattern arrives.

    pip install agentline
    export AGENTLINE_API_KEY=ag_live_...
    python custom_otp_pattern.py
"""

import os
import re
from agentline import Agentline

client = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])

number = client.provision_number(area_code="415")
print(f"Phone: {number.phone_number}  — paste into the signup form.")

# Alphanumeric 8-character code like "A3F7BK92"
alphanumeric = r"[A-Z0-9]{8}"

# Or a strict 4-digit PIN
four_digit_pin = r"\b\d{4}\b"

# Or "Your code is: 123456" — capture just the digits
labeled = r"code is:?\s*(\d{6})"

msg = client.wait_for_sms(number.phone_number, timeout=180, match=alphanumeric)

if msg is None:
    print("Timed out waiting for code.")
else:
    print(f"Full message body: {msg.body}")
    m = re.search(alphanumeric, msg.body)
    print(f"Extracted code: {m.group(0) if m else '(no match)'}")

client.release_number(number.phone_number)
