"""Agentline as LangChain Tools.

Wraps SDK methods as `@tool`-decorated functions an agent executor can call.
Shows a minimal LangChain ReAct agent that signs up for a service by
capturing a 2FA code on its own.

    pip install agentline langchain langchain-anthropic
    export AGENTLINE_API_KEY=ag_live_...
    export ANTHROPIC_API_KEY=sk-ant-...
    python integration_langchain.py
"""

import os
from agentline import Agentline
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

agent_api = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])


@tool
def provision_number(area_code: str = "415") -> str:
    """Provision a fresh phone number; returns the E.164 string."""
    n = agent_api.provision_number(area_code=area_code)
    return n.phone_number


@tool
def wait_for_sms_code(phone_number: str, timeout: int = 120) -> str:
    """Wait up to `timeout` seconds for an SMS verification code on the given number. Returns the extracted code or 'TIMEOUT'."""
    code = agent_api.get_verification_code(phone_number, timeout=float(timeout))
    return code or "TIMEOUT"


@tool
def release_number(phone_number: str) -> str:
    """Release a provisioned phone number."""
    return "released" if agent_api.release_number(phone_number) else "failed"


prompt = ChatPromptTemplate.from_messages([
    ("system", "You have Agentline tools to provision numbers and capture SMS codes."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

llm = ChatAnthropic(model="claude-sonnet-4-6-20250929")
tools = [provision_number, wait_for_sms_code, release_number]
executor = AgentExecutor(
    agent=create_tool_calling_agent(llm, tools, prompt),
    tools=tools,
    verbose=True,
)

result = executor.invoke({
    "input": "Provision a 415 number. Tell me the number. Wait 60s for an SMS code. Release the number. Return the code.",
})
print(result["output"])
