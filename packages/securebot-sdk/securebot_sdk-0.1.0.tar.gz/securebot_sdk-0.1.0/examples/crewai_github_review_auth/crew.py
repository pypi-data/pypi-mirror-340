from openinference.instrumentation.crewai import CrewAIInstrumentor
import os
from pathlib import Path

import yaml
from securebot_sdk.core import IdentityProvider
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from tools import get_pr_details_tool, get_pr_list_tool, get_pr_review_tool
from openinference.instrumentation.openai import OpenAIInstrumentor


# Load environment variables
load_dotenv()

# Initialize the OpenID client and get IAM context
identity_provider = IdentityProvider(
    project_id=os.getenv("AGENT_AUTH_PROJECT_ID"),
    client_id=os.getenv("AGENT_AUTH_CLIENT_ID"),
    client_secret=os.getenv("AGENT_AUTH_CLIENT_SECRET"),
    tracing=True,
)

# tracing = Tracing()
# trace_provider = tracing.setup()

OpenAIInstrumentor().instrument()
CrewAIInstrumentor().instrument()

ctx_pr_analyzer_agent = identity_provider.create_agent_context("pr-analyzer-agent")
ctx_code_reviewer_agent = identity_provider.create_agent_context("code-reviewer-agent")
ctx_pr_reviewer_agent = identity_provider.create_agent_context("pr-reviewer-agent")


@CrewBase
class GitHubPRReviewCrew:
    """GitHub PR Review Crew."""

    agents_config_path = "config/agents.yaml"
    tasks_config_path = "config/tasks.yaml"

    def __init__(self, repo_name: str):
        self.repo_name = repo_name
        self.agents_config = yaml.safe_load(Path(self.agents_config_path).read_text())
        self.tasks_config = yaml.safe_load(Path(self.tasks_config_path).read_text())

    @agent
    def pr_analyzer_agent(self) -> Agent:
        """Analyze PRs and identify key aspects for review."""
        return Agent(
            config=self.agents_config["pr_analyzer"],
            verbose=True,
            tools=[
                get_pr_list_tool(
                    repo_name=self.repo_name, agent_iam_role="pr-analyzer-agent"
                ),
                get_pr_details_tool(
                    repo_name=self.repo_name, agent_iam_role="pr-analyzer-agent"
                ),
            ],
        )

    @agent
    def code_reviewer_agent(self) -> Agent:
        """Review code changes in PRs."""
        return Agent(
            config=self.agents_config["code_reviewer"],
            verbose=True,
            tools=[
                get_pr_details_tool(
                    repo_name=self.repo_name, agent_iam_role="code-reviewer-agent"
                )
            ],
        )

    @agent
    def pr_reviewer_agent(self) -> Agent:
        """Create comprehensive PR reviews."""
        return Agent(
            config=self.agents_config["pr_reviewer"],
            verbose=True,
            tools=[
                get_pr_review_tool(
                    repo_name=self.repo_name, agent_iam_role="pr-reviewer-agent"
                )
            ],
        )

    @task
    def analyze_prs(self) -> Task:
        """Analyze all open PRs in the repository."""
        return Task(
            config=self.tasks_config["analyze_prs"],
            agent=self.pr_analyzer_agent(),
        )

    @task
    def review_code_changes(self) -> Task:
        """Review code changes in each PR."""
        return Task(
            config=self.tasks_config["review_code_changes"],
            agent=self.code_reviewer_agent(),
        )

    @task
    def create_pr_reviews(self) -> Task:
        """Create one clean review for each PR."""
        return Task(
            config=self.tasks_config["create_pr_reviews"],
            agent=self.pr_reviewer_agent(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GitHub PR Review crew."""
        return Crew(
            agents=[
                self.pr_analyzer_agent(),
                self.code_reviewer_agent(),
                self.pr_reviewer_agent(),
            ],
            tasks=[
                self.analyze_prs(),
                self.review_code_changes(),
                self.create_pr_reviews(),
            ],
            process=Process.sequential,
            verbose=True,
        )
