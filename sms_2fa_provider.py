"""Issue 2FA codes to YOUR users via Agentline.

The inverse of `sms_2fa_signup.py` — instead of receiving codes, you're
sending them. Use this when YOUR app needs to send verification codes
(not relying on Twilio/Vonage directly).

Flask endpoint style: POST /send-code { phone } issues a 6-digit code,
persists it with a 10-minute expiry, sends it via Agentline.

    pip install agentline flask
    export AGENTLINE_API_KEY=ag_live_...
    export FROM_NUMBER=+14155551234
    python sms_2fa_provider.py
"""

import os
import secrets
import time
from flask import Flask, jsonify, request
from agentline import Agentline

agent = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])
FROM_NUMBER = os.environ["FROM_NUMBER"]

app = Flask(__name__)
pending: dict[str, tuple[str, float]] = {}


@app.post("/send-code")
def send_code():
    phone = request.json["phone"]
    code = f"{secrets.randbelow(1_000_000):06d}"
    pending[phone] = (code, time.time() + 600)  # 10 min expiry
    agent.send_sms(
        from_=FROM_NUMBER,
        to=phone,
        body=f"Your Acme Boots verification code is {code}. Valid for 10 minutes.",
    )
    return jsonify({"status": "sent"})


@app.post("/verify-code")
def verify_code():
    phone = request.json["phone"]
    code = request.json["code"]
    stored = pending.get(phone)
    if not stored or stored[1] < time.time():
        return jsonify({"status": "expired"}), 400
    if stored[0] != code:
        return jsonify({"status": "invalid"}), 400
    del pending[phone]
    return jsonify({"status": "verified"})


if __name__ == "__main__":
    app.run(port=5000)
