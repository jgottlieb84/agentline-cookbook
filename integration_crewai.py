"""Agentline inside a CrewAI multi-agent crew.

A two-agent crew: a `Recruiter` agent that provisions disposable phone
numbers and a `Screener` agent that uses those numbers to capture 2FA
codes for candidate signups. Uses CrewAI's `@tool` decorator.

    pip install agentline crewai
    export AGENTLINE_API_KEY=ag_live_...
    python integration_crewai.py
"""

import os
from agentline import Agentline
from crewai import Agent, Crew, Task
from crewai.tools import tool

a = Agentline(api_key=os.environ["AGENTLINE_API_KEY"])


@tool("provision_number")
def provision_number_tool(area_code: str = "415") -> str:
    """Provision a fresh phone number. Returns E.164 string."""
    return a.provision_number(area_code=area_code).phone_number


@tool("capture_code")
def capture_code_tool(phone_number: str, since: str) -> str:
    """Wait on the existing number; since is the UTC timestamp before signup."""
    return str(a.get_verification_code(phone_number, since=since, timeout=120))


@tool("release_number")
def release_number_tool(phone_number: str) -> str:
    """Release a provisioned number."""
    return "ok" if a.release_number(phone_number) else "failed"


recruiter = Agent(
    role="Recruiter",
    goal="Provision a fresh phone number for each candidate",
    backstory="You handle identity provisioning for candidate screenings.",
    tools=[provision_number_tool, release_number_tool],
)

screener = Agent(
    role="Screener",
    goal="Complete service signups that require phone verification",
    backstory="You run the signup flow and capture verification codes.",
    tools=[capture_code_tool],
)

t1 = Task(
    description="Provision a 415 phone number for candidate Alice Chen.",
    agent=recruiter,
    expected_output="The provisioned phone number in E.164 format.",
)
t2 = Task(
    description="Use the capture_code tool to complete Alice's signup and return the code.",
    agent=screener,
    expected_output="The 2FA code as a string.",
)

crew = Crew(agents=[recruiter, screener], tasks=[t1, t2])
print(crew.kickoff())
