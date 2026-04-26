"""Send a simple newsletter to a list from a CSV.

Reads `subscribers.csv` with columns (email, first_name) and sends each
a personalized message. For real campaigns add an unsubscribe link.

    pip install agentline
    export AGENTLINE_API_KEY=ag_live_...
    export FROM_EMAIL=hello@mail.agentline.co
    python email_newsletter.py
"""

import csv
import os
from agentline import Agentline

agent = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])
FROM_EMAIL = os.environ["FROM_EMAIL"]

SUBJECT = "New arrivals: the spring boot collection is live"
BODY_TEMPLATE = """Hi {first_name},

Spring is here and so are our new styles. The full collection is live now:
https://acmeboots.example/spring

As a thank you for reading, use code SPRING10 for 10% off through April 30.

— The Acme Boots team

---
To unsubscribe, reply STOP.
"""

with open("subscribers.csv") as f:
    for row in csv.DictReader(f):
        body = BODY_TEMPLATE.format(first_name=row["first_name"])
        agent.send_email(
            from_=FROM_EMAIL,
            to=row["email"],
            subject=SUBJECT,
            body=body,
        )
        print(f"sent to {row['email']}")
