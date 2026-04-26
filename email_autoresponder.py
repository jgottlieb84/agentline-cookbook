"""AI replies to inbound emails automatically.

Waits for inbound email, uses Claude to draft a reply, sends it back.
Stateless; extend with conversation history + thread tracking for
production.

    pip install agentline anthropic
    export AGENTLINE_API_KEY=ag_live_...
    export ANTHROPIC_API_KEY=sk-ant-...
    export SUPPORT_EMAIL=support@mail.agentline.co
    python email_autoresponder.py
"""

import os
from agentline import Agentline
from anthropic import Anthropic

agent = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])
claude = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
SUPPORT_EMAIL = os.environ["SUPPORT_EMAIL"]

SYSTEM = (
    "You are a friendly first-line support rep for Acme Boots. "
    "Reply in 2–4 sentences. Be specific. If you cannot solve the "
    "issue, say so and promise a human will follow up within 24 hours."
)

print(f"Listening for inbound email on {SUPPORT_EMAIL}...  Ctrl+C to stop.")

while True:
    msg = agent.wait_for_email(SUPPORT_EMAIL, timeout=120)
    if msg is None:
        continue

    print(f"\n<- {msg.from_email}: {msg.subject}")

    reply = claude.messages.create(
        model="claude-sonnet-4-6-20250929",
        max_tokens=600,
        system=SYSTEM,
        messages=[{
            "role": "user",
            "content": f"Subject: {msg.subject}\n\n{msg.body_text}",
        }],
    ).content[0].text

    agent.send_email(
        from_=SUPPORT_EMAIL,
        to=msg.from_email,
        subject=f"Re: {msg.subject}",
        body=reply,
    )
    print(f"-> {msg.from_email}: {reply[:80]}...")
