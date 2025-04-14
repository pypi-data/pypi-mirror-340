from pathlib import Path

import yaml
from securebot_sdk.core import AgentAuth
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from task import (
    filings_analysis_task,
    financial_analysis_task,
    recommend_task,
    research_task,
)
from tools import (
    calculator_tool,
    scrap_website_tool,
    sec10k_tool,
    sec10q_tool,
    website_search_tool,
)

from phoenix.otel import register

tracer_provider = register(
    endpoint="http://localhost:6006/v1/traces",
    project_name="default",  # sets a project name for spans
    batch=True,  # uses a batch span processor
    auto_instrument=True,  # uses all installed OpenInference instrumentors
)

load_dotenv()

# Initialize the OpenID client and get IAM context
agent_auth = AgentAuth(
    project_id="67de040bd035345b15a6599e",
    client_id="975932d6-d92c-4a7e-b15d-adaad55aaf57",
    client_secret="Voa1p0oLC3DEujhcQ4MKs4nZXh9tg6Ih",
)

ctx_financial_analyst_agent = agent_auth.create_agent_context("financial-analyst-agent")
ctx_research_analyst_agent = agent_auth.create_agent_context("research-analyst-agent")
ctx_investment_advisor_agent = agent_auth.create_agent_context(
    "investment-advisor-agent"
)


@CrewBase
class StockAnalysisCrew:
    """Stock Analysis Crew."""

    agents_config_path = "config/agents.yaml"
    tasks_config_path = "config/tasks.yaml"

    def __init__(self):
        self.agents_config = yaml.safe_load(Path(self.agents_config_path).read_text())
        self.tasks_config = yaml.safe_load(Path(self.tasks_config_path).read_text())

    @agent
    def financial_analyst_agent(self) -> Agent:
        """Analyze the financial data of a company."""
        return Agent(
            config=self.agents_config["financial_analyst"],
            verbose=True,
            tools=[
                website_search_tool(agent_iam_role="financial-analyst-agent"),
                scrap_website_tool(agent_iam_role="financial-analyst-agent"),
                calculator_tool(agent_iam_role="financial-analyst-agent"),
                sec10k_tool(agent_iam_role="financial-analyst-agent", ticker="AMZN"),
                sec10q_tool(agent_iam_role="financial-analyst-agent", ticker="AMZN"),
            ],
        )

    @task
    def financial_analysis(self) -> Task:
        """Analyze the financial data of a company."""
        return financial_analysis_task(
            agent_iam_role="financial-analyst-agent",
            config=self.tasks_config["financial_analysis"],
            agent=self.financial_analyst_agent(),
        )

    @task
    def filings_analysis(self) -> Task:
        """Analyze the financial data of a company."""
        return filings_analysis_task(
            agent_iam_role="financial-analyst-agent",
            config=self.tasks_config["filings_analysis"],
            agent=self.financial_analyst_agent(),
        )

    @agent
    def research_analyst_agent(self) -> Agent:
        """Research and analyze company information."""
        return Agent(
            config=self.agents_config["research_analyst"],
            verbose=True,
            tools=[
                scrap_website_tool(agent_iam_role="research-analyst-agent"),
                sec10k_tool(agent_iam_role="research-analyst-agent", ticker="AMZN"),
                sec10q_tool(agent_iam_role="research-analyst-agent", ticker="AMZN"),
            ],
        )

    @task
    def research(self) -> Task:
        """Research company information."""
        return research_task(
            agent_iam_role="research-analyst-agent",
            config=self.tasks_config["research"],
            agent=self.research_analyst_agent(),
        )

    @agent
    def investment_advisor_agent(self) -> Agent:
        """Provide investment recommendations."""
        return Agent(
            config=self.agents_config["investment_advisor"],
            verbose=True,
            tools=[
                website_search_tool(agent_iam_role="investment-advisor-agent"),
                scrap_website_tool(agent_iam_role="investment-advisor-agent"),
                calculator_tool(agent_iam_role="investment-advisor-agent"),
            ],
        )

    @task
    def recommend(self) -> Task:
        """Recommend a company to invest in."""
        return recommend_task(
            agent_iam_role="investment-advisor-agent",
            config=self.tasks_config["recommend"],
            agent=self.investment_advisor_agent(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Stock Analysis crew."""
        return Crew(
            agents=[
                self.financial_analyst_agent(),
                self.research_analyst_agent(),
                self.investment_advisor_agent(),
            ],
            tasks=[
                self.financial_analysis(),
                self.filings_analysis(),
                self.research(),
                self.recommend(),
            ],
            process=Process.sequential,
            verbose=True,
        )
