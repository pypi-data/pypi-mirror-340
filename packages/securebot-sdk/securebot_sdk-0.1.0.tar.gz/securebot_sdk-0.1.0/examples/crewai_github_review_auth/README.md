# GitHub PR Review System

A system for automated GitHub Pull Request reviews using CrewAI and direct GitHub REST API integration. This system provides two ways to review PRs:
1. Direct tool usage for precise control
2. CrewAI-based automated review process

## Features

- List and analyze open pull requests
- Get detailed PR information including files, commits, and comments
- Create comprehensive PR reviews
- Support for both GitHub.com and GitHub Enterprise
- Custom headers and base URL configuration
- Two modes of operation:
  - Direct tool usage
  - CrewAI-based automated review

## Prerequisites

- Python 3.9 or higher
- GitHub Personal Access Token with appropriate permissions
- Agent Auth credentials

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd github-pr-review
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Configure environment variables:
Create a `.env` file in the project root with the following variables:
```env
# GitHub Configuration
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=owner/repo

# Agent Auth Configuration
AGENT_AUTH_PROJECT_ID=your_project_id
AGENT_AUTH_CLIENT_ID=your_client_id
AGENT_AUTH_CLIENT_SECRET=your_client_secret
```

## Usage

### Direct Tool Usage

The system provides three main tools that can be used directly:

1. **PR List Tool**: Get all open PRs
```python
from tools import get_pr_list_tool

tool = get_pr_list_tool(
    repo_name="owner/repo",
    token="your_token",
    agent_iam_role="reviewer"
)
prs = tool.get_open_prs()
```

2. **PR Details Tool**: Get detailed information about a PR
```python
from tools import get_pr_details_tool

tool = get_pr_details_tool(
    repo_name="owner/repo",
    token="your_token",
    agent_iam_role="reviewer"
)
details = tool.get_pr_details(pr_number=123)
```

3. **PR Review Tool**: Create reviews for PRs
```python
from tools import get_pr_review_tool

tool = get_pr_review_tool(
    repo_name="owner/repo",
    token="your_token",
    agent_iam_role="reviewer"
)
review = tool.create_pr_review(
    pr_number=123,
    body="Great work!",
    event="APPROVE"
)
```

### CrewAI Mode

Run the automated review process using CrewAI:

```bash
python main.py
```

When prompted, choose mode 2 for CrewAI-based review.

## Configuration

### GitHub Enterprise

To use with GitHub Enterprise, set the base URL:

```python
tool = get_pr_list_tool(
    repo_name="owner/repo",
    token="your_token",
    agent_iam_role="reviewer",
    base_url="https://github.your-enterprise.com/api/v3"
)
```

### Custom Headers

Add custom headers to API requests:

```python
tool = get_pr_list_tool(
    repo_name="owner/repo",
    token="your_token",
    agent_iam_role="reviewer",
    headers={
        "X-Custom-Header": "value",
        "Accept": "application/vnd.github.v3+json"
    }
)
```

## Development

Install development dependencies:
```bash
pip install -e ".[dev]"
```

Run tests:
```bash
pytest
```

Format code:
```bash
black .
isort .
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
