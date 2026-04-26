"""Agentline as tools in a direct Anthropic SDK tool-use loop.

No framework — just the Anthropic SDK and Agentline. Claude decides
which Agentline operation to run, we execute it, feed the result back,
loop until Claude is done.

    pip install agentline anthropic
    export AGENTLINE_API_KEY=ag_live_...
    export ANTHROPIC_API_KEY=sk-ant-...
    python integration_anthropic_tool_use.py
"""

import os
from agentline import Agentline
from anthropic import Anthropic

a = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])
claude = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

TOOLS = [
    {
        "name": "provision_number",
        "description": "Provision a phone number. Returns {phone_number, id}.",
        "input_schema": {
            "type": "object",
            "properties": {"area_code": {"type": "string"}},
            "required": [],
        },
    },
    {
        "name": "wait_for_sms_code",
        "description": "Block up to timeout seconds for an SMS code on a number. Returns {code} or {code: null} on timeout.",
        "input_schema": {
            "type": "object",
            "properties": {
                "phone_number": {"type": "string"},
                "timeout": {"type": "number", "default": 120},
            },
            "required": ["phone_number"],
        },
    },
    {
        "name": "release_number",
        "description": "Release a provisioned phone number.",
        "input_schema": {
            "type": "object",
            "properties": {"phone_number": {"type": "string"}},
            "required": ["phone_number"],
        },
    },
]


def execute_tool(name: str, args: dict) -> dict:
    if name == "provision_number":
        n = a.provision_number(area_code=args.get("area_code"))
        return {"phone_number": n.phone_number, "id": n.id}
    if name == "wait_for_sms_code":
        code = a.get_verification_code(args["phone_number"], timeout=args.get("timeout", 120))
        return {"code": code}
    if name == "release_number":
        return {"released": a.release_number(args["phone_number"])}
    return {"error": f"unknown tool {name}"}


messages = [{
    "role": "user",
    "content": "Provision a 415 number, wait 90 seconds for a code, release it, and give me the code.",
}]

while True:
    resp = claude.messages.create(
        model="claude-sonnet-4-6-20250929",
        max_tokens=1024,
        tools=TOOLS,
        messages=messages,
    )
    messages.append({"role": "assistant", "content": resp.content})

    if resp.stop_reason != "tool_use":
        for block in resp.content:
            if block.type == "text":
                print(block.text)
        break

    tool_results = []
    for block in resp.content:
        if block.type == "tool_use":
            output = execute_tool(block.name, block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": str(output),
            })
    messages.append({"role": "user", "content": tool_results})
