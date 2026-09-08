"""Request a human code without reading an authenticator or sending messages.

Requires Agentline SDK 0.3 source. Set AGENTLINE_API_KEY, AGENTLINE_BASE_URL,
and AGENTLINE_RECIPIENT_EMAIL. Share the returned private link with the
person through your existing conversation. Never log the submitted code.
"""
import os
import time
from agentline import Agentline

with Agentline(os.environ["AGENTLINE_API_KEY"], base_url=os.environ["AGENTLINE_BASE_URL"]) as client:
    request = client.request_human_code(
        application_url="https://example.com/login",
        action="Authorize the sign-in we discussed for your account",
        recipient_email=os.environ["AGENTLINE_RECIPIENT_EMAIL"],
        agent_name="My assistant",
    )
    print("Share privately with the named recipient:", request["approval_url"])
    deadline = time.monotonic() + 280
    while time.monotonic() < deadline:
        state = client.get_human_request(request["id"])
        if state["status"] == "submitted":
            result = client.consume_human_code(request["id"])
            # Submit result["code"] only to the login flow described above.
            # Do not print it, save it, or repeat it in a review.
            break
        if state["status"] != "pending":
            print("Request closed:", state["status"])
            break
        time.sleep(3)
    else:
        client.cancel_human_request(request["id"])
