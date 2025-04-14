import os

from crew import GitHubPRReviewCrew
from dotenv import load_dotenv
from tools import get_pr_details_tool, get_pr_list_tool, get_pr_review_tool

load_dotenv()


def run_direct_tools():
    """Demonstrate direct usage of the GitHub tools."""
    # Get configuration from environment
    repo_name = os.getenv("GITHUB_REPO", "securebotinc/ai-gateway")

    # Initialize tools
    pr_list_tool = get_pr_list_tool(
        repo_name=repo_name,
    )

    # Get all open PRs
    prs = pr_list_tool.get_open_prs()
    print(f"Found {len(prs)} open PRs")

    for pr in prs:
        print(f"\nReviewing PR #{pr['number']}: {pr['title']}")

        # Get PR details
        pr_details_tool = get_pr_details_tool(
            repo_name=repo_name,
        )
        details = pr_details_tool.get_pr_details(pr["number"])

        # Create review
        pr_review_tool = get_pr_review_tool(
            repo_name=repo_name,
        )

        # Example review based on PR details
        review_body = f"""
        Review for PR #{pr['number']}: {pr['title']}

        Changes:
        - Files changed: {len(details['files_changed'])}
        - Commits: {len(details['commits'])}

        Summary:
        This PR introduces changes to {', '.join(details['files_changed'][:3])} and more.
        The changes look good overall, but please consider adding tests for the new functionality.
        """

        review = pr_review_tool.create_pr_review(
            pr_number=pr["number"], body=review_body, event="COMMENT"
        )
        print(f"Created review: {review['id']}")


def run_crew():
    """Run the PR review crew."""
    crew = GitHubPRReviewCrew(
        repo_name=os.getenv("GITHUB_REPO", "securebotinc/ai-gateway"),
    )
    return crew.crew().kickoff()


if __name__ == "__main__":
    print("## Welcome to GitHub PR Review System")
    print("----------------------------------")

    # Choose between direct tools or crew
    mode = input("Choose mode (1: Direct Tools, 2: Crew): ")

    if mode == "1":
        print("\nRunning with direct tools...")
        run_direct_tools()
    else:
        print("\nRunning with crew...")
        result = run_crew()
        print("\n\n########################")
        print("## PR Review Results")
        print("########################\n")
        print(result)
