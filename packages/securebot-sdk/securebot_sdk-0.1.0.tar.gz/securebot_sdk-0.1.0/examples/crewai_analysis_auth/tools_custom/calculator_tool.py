from typing import Any

from crewai.tools import BaseTool


class CalculatorTool(BaseTool):
    """Useful to perform any mathematical calculations, like sum, minus, multiplication, division, etc.
    The input to this tool should be a mathematical  expression, a couple examples are `200*7` or `5000/2*10."""

    name: str = "Calculator tool"
    description: str = """Useful to perform any mathematical calculations, like sum, minus, multiplication, division, etc.
    The input to this tool should be a mathematical  expression, a couple examples are `200*7` or `5000/2*10."""

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """Perform a mathematical calculation."""
        if not args:
            raise ValueError("No operation provided")
        return eval(args[0])  # noqa: S308
