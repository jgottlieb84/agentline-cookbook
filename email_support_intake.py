"""Triage inbound support emails with Claude.

Each inbound email is classified into {billing, technical, sales, spam}
and routed to the appropriate team via a follow-up email. Replace the
`route_to_team` function with your actual ticketing-system integration.

    pip install agentline anthropic
    export AGENTLINE_API_KEY=ag_live_...
    export ANTHROPIC_API_KEY=sk-ant-...
    export SUPPORT_EMAIL=hello@mail.agentline.co
    python email_support_intake.py
"""

import json
import os
from agentline import Agentline
from anthropic import Anthropic

agent = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])
claude = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
SUPPORT_EMAIL = os.environ["SUPPORT_EMAIL"]

ROUTING = {
    "billing": "billing@acmeboots.example",
    "technical": "eng-oncall@acmeboots.example",
    "sales": "sales@acmeboots.example",
    "spam": None,  # dropped
}

CLASSIFIER_PROMPT = """
Classify the following customer email into exactly one category:
billing, technical, sales, spam.

Reply with ONLY a JSON object: {"category": "...", "priority": "low|med|high"}
"""


def route_to_team(category: str, message) -> None:
    target = ROUTING[category]
    if not target:
        return
    agent.send_email(
        from_=SUPPORT_EMAIL,
        to=target,
        subject=f"[{category}] {message.subject}",
        body=f"From: {message.from_email}\n\n{message.body_text}",
    )


while True:
    msg = agent.wait_for_email(SUPPORT_EMAIL, timeout=120)
    if msg is None:
        continue

    result = claude.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        system=CLASSIFIER_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Subject: {msg.subject}\n\n{msg.body_text}",
        }],
    ).content[0].text

    verdict = json.loads(result)
    print(f"{msg.from_email}: {verdict}")
    route_to_team(verdict["category"], msg)
