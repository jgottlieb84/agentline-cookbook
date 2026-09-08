"""Sign up for multiple services with a fresh identity per service.

For each service in the list, mint a new phone number, drive a signup
(here mocked as a `signup_to(service, phone)` call — replace with your
actual browser-automation or API-based signup), capture the code, release.

Shows how the SDK scales to batch automation with no shared state.

    pip install agentline
    export AGENTLINE_API_KEY=ag_live_...
    python bulk_signup.py
"""

import os
from agentline import Agentline

client = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])

SERVICES = ["substack.com", "medium.com", "dev.to", "hashnode.com"]


def signup_to(service: str, phone: str) -> None:
    # Replace with real automation: Playwright, a form POST, whatever.
    # The point: you now have a throwaway phone number you can use anywhere.
    print(f"  → pretending to sign up at {service} with phone {phone}")


for service in SERVICES:
    print(f"Signing up for {service}...")
    phone, code = client.capture_code(area_code="415", timeout=120, on_provision=lambda phone: signup_to(service, phone))
    print(f"  phone: {phone}, code: {code}")
    print(f"  done. Number released.\n")
