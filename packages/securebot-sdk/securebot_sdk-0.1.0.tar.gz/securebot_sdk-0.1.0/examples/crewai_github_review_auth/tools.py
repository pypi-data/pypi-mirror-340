from securebot_sdk.identity.crewai import requires_tool_scope
from tools_custom.github_rest_tools import (
    GitHubPRDetailsTool,
    GitHubPRListTool,
    GitHubPRReviewTool,
)


@requires_tool_scope(scope="app:tool:GitHubPRListTool", pass_token=True)
def get_pr_list_tool(
    repo_name: str,
    token: str,
) -> GitHubPRListTool:
    """Get a tool for listing GitHub pull requests."""
    return GitHubPRListTool(repo_name=repo_name, token=token)


@requires_tool_scope(scope="app:tool:GitHubPRDetailsTool", pass_token=True)
def get_pr_details_tool(
    repo_name: str,
    token: str,
) -> GitHubPRDetailsTool:
    """Get a tool for getting detailed information about a pull request."""
    return GitHubPRDetailsTool(repo_name=repo_name, token=token)


@requires_tool_scope(scope="app:tool:GitHubPRReviewTool", pass_token=True)
def get_pr_review_tool(
    repo_name: str,
    token: str,
) -> GitHubPRReviewTool:
    """Get a tool for creating pull request reviews."""
    return GitHubPRReviewTool(repo_name=repo_name, token=token)
