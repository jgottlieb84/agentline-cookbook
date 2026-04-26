"""Send SMS appointment reminders the day before.

Reads an `appointments.csv` (patient_phone, patient_name, iso_datetime)
and sends each patient a reminder 24 hours before their slot. Intended
to run as a daily cron job.

    pip install agentline
    export AGENTLINE_API_KEY=ag_live_...
    export FROM_NUMBER=+14155551234
    python sms_appointment_reminders.py
"""

import csv
import os
from datetime import datetime, timedelta, timezone
from agentline import Agentline

agent = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])
FROM_NUMBER = os.environ["FROM_NUMBER"]

now = datetime.now(timezone.utc)
window_start = now + timedelta(hours=23)
window_end = now + timedelta(hours=25)


def format_reminder(name: str, when: datetime) -> str:
    local = when.astimezone()
    return (
        f"Hi {name}, this is Dr. Reyes's office reminding you of your "
        f"appointment tomorrow at {local:%-I:%M %p}. Reply C to confirm "
        f"or R to reschedule."
    )


with open("appointments.csv") as f:
    for row in csv.DictReader(f):
        slot = datetime.fromisoformat(row["iso_datetime"])
        if window_start <= slot <= window_end:
            body = format_reminder(row["patient_name"], slot)
            agent.send_sms(from_=FROM_NUMBER, to=row["patient_phone"], body=body)
            print(f"reminded {row['patient_name']} ({row['patient_phone']})")
