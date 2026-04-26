"""Sequential outbound SMS drip: day 0, day 2, day 7 messages to a list.

Loads a simple state file (`drip_state.json`) that tracks which day each
contact is on. Run this as a daily cron: it sends the right message
for whatever day each contact is currently on.

    pip install agentline
    export AGENTLINE_API_KEY=ag_live_...
    export FROM_NUMBER=+14155551234
    python sms_drip_campaign.py
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta, timezone
from agentline import Agentline

agent = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])
FROM_NUMBER = os.environ["FROM_NUMBER"]

SCHEDULE = {
    0: "Welcome to Acme Boots! Your 10% new-customer code is WELCOME10.",
    2: "Did your boots arrive? Reply with any questions — a real person reads these.",
    7: "One week in — how are they feeling? We'd love a quick review at acmeboots.example/review",
}

STATE = Path("drip_state.json")
state = json.loads(STATE.read_text()) if STATE.exists() else {}

for phone, entry in state.items():
    enrolled_at = datetime.fromisoformat(entry["enrolled_at"])
    days_in = (datetime.now(timezone.utc) - enrolled_at).days
    last_sent_day = entry.get("last_sent_day", -1)

    for day in sorted(SCHEDULE.keys()):
        if days_in >= day > last_sent_day:
            agent.send_sms(from_=FROM_NUMBER, to=phone, body=SCHEDULE[day])
            entry["last_sent_day"] = day
            print(f"sent day-{day} to {phone}")

STATE.write_text(json.dumps(state, indent=2))
