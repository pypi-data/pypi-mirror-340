from securebot_sdk.agent_auth.crewai import requires_task_scope
from crewai import Task


@requires_task_scope(scope="app:task:FinancialAnalysis")
def financial_analysis_task(config, agent) -> Task:
    """Analyze the financial data of a company."""
    return Task(config=config, agent=agent)


@requires_task_scope(scope="app:task:Research")
def research_task(config, agent) -> Task:
    """Research a company's financial data."""
    return Task(config=config, agent=agent)


@requires_task_scope(scope="app:task:FilingsAnalysis")
def filings_analysis_task(config, agent) -> Task:
    """Analyze a company's SEC filings."""
    return Task(config=config, agent=agent)


@requires_task_scope(scope="app:task:Recommend")
def recommend_task(config, agent) -> Task:
    """Recommend a company to invest in."""
    return Task(config=config, agent=agent)
