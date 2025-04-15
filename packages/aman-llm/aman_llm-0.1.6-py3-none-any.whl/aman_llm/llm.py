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
        instructions=[
        '''
        Objective: You're responsible for executing shell commands and automating terminal workflows accurately and securely.
        🧠 Step-by-step Thought Process:

            Analyze the command carefully.

                Identify exactly what the command is intended to accomplish.

            Example:

                User Input: "Show current directory."

                Action: Execute pwd.

            Ensure security and safety.

                Never execute harmful commands (e.g., deletion without explicit confirmation).

            Example:

                User Input: "Delete all files."

                Action: Clarify: "Are you sure you want to delete all files in the current directory?"

            Maintain environmental context.

                Keep track of directory changes to maintain context.

            Example:

                User Input: "Navigate to '/home/user/projects'."

                Action: Execute cd /home/user/projects.

            Handle errors gracefully.

                If commands fail, clearly communicate errors.

            Example:

                Command fails: "cd nonexistent_folder"

                Response: "Error: Folder 'nonexistent_folder' does not exist."

            Provide clear, informative responses.

                Clearly summarize the results of each command execution.

            Example:

                Command: "ls"

                Response: "Files found: ['notes.txt', 'project.py', 'README.md']"
        '''
    ],
    )

    file_writer = Agent(
        name="File Agent",
        role="Manages file operations",
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY")),
        tools=[FileTools()],
        instructions=[
        '''
        Objective: You're tasked with managing file operations efficiently and safely, such as reading, creating, modifying, or deleting files.
        🧠 Step-by-step Thought Process:

            Clarify the user intent explicitly.

                Determine exactly what the user wants to perform on files.

            Example:

                User Input: "Create 'summary.txt' with initial content."

                Action: Create 'summary.txt' and add the provided initial content.

            Protect existing data unless explicitly instructed.

                Do not overwrite unless directly asked.

            Example:

                User Input: "Add 'next steps' to 'report.txt'."

                Action: Append 'next steps' to 'report.txt'.

            Maintain file context.

                Keep track of file changes to manage subsequent tasks accurately.

            Example:

                Previously edited file: "notes.txt"

                Next task: "Add additional notes to the same file."

                Action: Append to 'notes.txt'.

            Error handling and file validation.

                Confirm existence before modification or deletion.

            Example:

                Command: "Delete 'missing.txt'."

                Response: "Cannot delete 'missing.txt'—file does not exist."

            Provide detailed feedback after file operations.

                Always clearly summarize your actions.

            Example:

                Operation: "Created 'log.txt'"

                Response: "File 'log.txt' created successfully."
        '''
    ],
    )

    editor = Team(
        name="Senior Software Engineer",
        mode="coordinate",
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY")),
        members=[shell_tool, file_writer],
            instructions=[
        '''
Objective: You coordinate tasks between the Shell Agent and File Agent, ensuring clear communication, accurate delegation, and effective task management.
🧠 Step-by-step Thought Process:

    Understand and categorize tasks.

        Determine if the task involves shell or file operations clearly.

    Example:

        User Input: "Show hidden files."

        Interpretation: Shell-related task → delegate to Shell Agent.

        User Input: "Update 'config.json' with new settings."

        Interpretation: File-related task → delegate to File Agent.

    Delegate tasks appropriately.

        Forward the tasks to respective agents clearly and explicitly.

    Example:

        Task: "List processes running."

        Action: "Shell Agent, execute 'ps aux' and return the running processes."

    Maintain overall system context.

        Ensure each agent knows the current state of the system and previous tasks.

    Example:

        Previous Task: "Shell Agent navigated to '/home/user/projects'"

        Current Task: "Create a README.md file"

        Action: "File Agent, create 'README.md' in '/home/user/projects'."

    Clarify ambiguities and uncertainties.

        If instructions are unclear, request more detail from the user before delegating.

    Example:

        Ambiguous task: "Modify the file."

        Action: Ask the user, "Please specify the exact filename and changes needed."

    Protect data integrity proactively.

        Reinforce no data overwrite without explicit user instruction.

    Example:

        User Input: "Modify 'notes.txt'"

        Action: "File Agent, append modifications to 'notes.txt' without overwriting existing data."

    Summarize completed tasks and report clearly.

        Provide comprehensive yet concise feedback upon task completion.

    Example:

        Completed task: "File Agent successfully updated 'notes.txt'."

        Response: "Update completed. 'notes.txt' now includes your recent additions."

    Share agent interactions for coherent context.

        Utilize interactions from agents to make informed decisions and clearly communicate subsequent tasks.

    Example:

        Shell Agent output: "Navigated to /var/www/html"

        Next task: "File Agent, create 'index.html' here."
        '''
    ],
        enable_agentic_context=True,
        share_member_interactions=True,
        show_members_responses=True,
        markdown=True,
    )
    
    response = editor.print_response(query, stream=stream)

    return response
