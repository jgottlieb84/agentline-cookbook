# Agentline Cookbook

Runnable recipes showing how to use Agentline (`pip install agentline`) for real-world AI agent tasks — provisioning numbers, capturing 2FA codes, placing AI voice calls, sending/receiving email.

## Setup

```bash
pip install -r requirements.txt
export AGENTLINE_API_KEY=ag_live_...   # get one at https://www.agentline.co
```

On Windows PowerShell:
```powershell
$env:AGENTLINE_API_KEY = "ag_live_..."
```

Each recipe is self-contained — run any file directly with `python <recipe>.py`.

## Recipes

### Verification & sign-ups
- [`sms_2fa_signup.py`](sms_2fa_signup.py) — provision a number, capture the SMS 2FA code, release
- [`email_2fa_signup.py`](email_2fa_signup.py) — same but for email-based verification
- [`disposable_identity.py`](disposable_identity.py) — ephemeral phone + email together, auto-released after use
- [`custom_otp_pattern.py`](custom_otp_pattern.py) — capture 4-digit, 8-digit, or alphanumeric OTPs via regex
- [`bulk_signup.py`](bulk_signup.py) — sign up for multiple services with a fresh identity per service

### Voice
- [`voice_appointment_confirm.py`](voice_appointment_confirm.py) — AI calls a patient to confirm an appointment
- [`voice_lead_qualifier.py`](voice_lead_qualifier.py) — AI calls a lead, qualifies them, returns a structured verdict
- [`voice_survey.py`](voice_survey.py) — AI calls users and asks a 3-question survey
- [`voice_medical_records.py`](voice_medical_records.py) — AI calls another doctor's office requesting records
- [`voice_restaurant_reservation.py`](voice_restaurant_reservation.py) — AI books a table for party of N

### SMS
- [`sms_customer_support_bot.py`](sms_customer_support_bot.py) — auto-reply to inbound SMS using Claude
- [`sms_appointment_reminders.py`](sms_appointment_reminders.py) — send reminders the day before an appointment
- [`sms_drip_campaign.py`](sms_drip_campaign.py) — sequential outbound SMS to a list, day-by-day
- [`sms_2fa_provider.py`](sms_2fa_provider.py) — issue your own 2FA codes to users via Agentline

### Email
- [`email_autoresponder.py`](email_autoresponder.py) — AI replies to inbound emails automatically
- [`email_newsletter.py`](email_newsletter.py) — send a newsletter to a list from a CSV
- [`email_support_intake.py`](email_support_intake.py) — triage inbound support emails with Claude

### Framework integrations
- [`integration_langchain.py`](integration_langchain.py) — Agentline as LangChain Tools
- [`integration_anthropic_tool_use.py`](integration_anthropic_tool_use.py) — Agentline as Claude tools (direct Anthropic SDK)
- [`integration_crewai.py`](integration_crewai.py) — Agentline as CrewAI Tools in a multi-agent crew

## MCP server

If you'd rather plug Agentline into Claude Desktop / Cursor / Zed / Windsurf instead of writing Python, install the [Agentline MCP server](https://pypi.org/project/agentline-mcp/):

```bash
uvx agentline-mcp
```

See https://registry.modelcontextprotocol.io/v0/servers?search=agentline for MCP client configuration.

## License

MIT. Copy, fork, ship.
