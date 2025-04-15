# llm.py
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.shell import ShellTools
from agno.tools.file import FileTools
from dotenv import load_dotenv
from agno.team.team import Team
import os

load_dotenv()

def llm_call(query: str, stream: bool = False):
    shell_tool = Agent(
        name="Shell Agent",
        role="Executes shell commands",
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY")),
        tools=[ShellTools()],
    )

    file_writer = Agent(
        name="File Agent",
        role="Manages file operations",
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY")),
        tools=[FileTools()],
    )

    editor = Team(
        name="Senior Software Engineer",
        mode="coordinate",
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY")),
        members=[shell_tool, file_writer],
        enable_agentic_context=True,
        share_member_interactions=True,
        show_members_responses=True,
        markdown=True,
    )
    
    response = editor.run_response(query, stream=stream)

    return response
