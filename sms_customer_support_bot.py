"""Auto-reply to inbound SMS using Claude.

Loops: wait for an inbound message, generate a reply with Claude, send
back via Agentline. Stateless for simplicity; in production persist the
conversation history keyed by the inbound phone number.

    pip install agentline anthropic
    export AGENTLINE_API_KEY=ag_live_...
    export ANTHROPIC_API_KEY=sk-ant-...
    export SUPPORT_NUMBER=+14155551234   # your provisioned support line
    python sms_customer_support_bot.py
"""

import os
from agentline import Agentline
from anthropic import Anthropic

agent = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])
claude = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
SUPPORT_NUMBER = os.environ["SUPPORT_NUMBER"]

SYSTEM = (
    "You are a friendly customer support agent for Acme Boots. "
    "Reply concisely (SMS character budget). If the question is about "
    "a return, direct them to returns@acmeboots.example. "
    "If you can't answer, ask them to email support@acmeboots.example."
)

print(f"Listening for inbound SMS on {SUPPORT_NUMBER}...  Ctrl+C to stop.")

while True:
    msg = agent.wait_for_sms(SUPPORT_NUMBER, timeout=120)
    if msg is None:
        continue

    print(f"\n<- {msg.from_number}: {msg.body}")

    reply = claude.messages.create(
        model="claude-sonnet-4-6-20250929",
        max_tokens=300,
        system=SYSTEM,
        messages=[{"role": "user", "content": msg.body}],
    ).content[0].text

    agent.send_sms(from_=SUPPORT_NUMBER, to=msg.from_number, body=reply)
    print(f"-> {msg.from_number}: {reply}")
