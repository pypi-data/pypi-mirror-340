from securebot_sdk.agent_auth.crewai import requires_tool_scope
from crewai_tools import ScrapeWebsiteTool, WebsiteSearchTool
from tools_custom import CalculatorTool, SEC10KTool, SEC10QTool


@requires_tool_scope(scope="app:tool:WebsiteSearchTool")
def website_search_tool() -> WebsiteSearchTool:
    """Search the web for information about a company."""
    return WebsiteSearchTool()


@requires_tool_scope(scope="app:tool:ScrapeWebsiteTool")
def scrap_website_tool() -> ScrapeWebsiteTool:
    """Scrape a website for information about a company."""
    return ScrapeWebsiteTool()


@requires_tool_scope(scope="app:tool:CalculatorTool")
def calculator_tool() -> CalculatorTool:
    """Calculate the result of an arithmetic operation."""
    return CalculatorTool()


@requires_tool_scope(scope="app:tool:SEC10KTool")
def sec10k_tool(ticker) -> SEC10KTool:
    """Get the SEC 10K filing for a company."""
    return SEC10KTool(ticker)


@requires_tool_scope(scope="app:tool:SEC10QTool")
def sec10q_tool(ticker) -> SEC10QTool:
    """Get the SEC 10Q filing for a company."""
    return SEC10QTool(ticker)
