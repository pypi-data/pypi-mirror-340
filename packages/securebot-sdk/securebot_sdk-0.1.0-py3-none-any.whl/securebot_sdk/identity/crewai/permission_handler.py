import functools
from concurrent.futures import Future
from typing import Any, Callable, Optional, Type, TypeVar, cast

from crewai import Task
from crewai.tasks.task_output import OutputFormat, TaskOutput
from crewai.tools import BaseTool

from securebot_sdk.core.identity_manager import IdentityManager
from securebot_sdk.core.permission_handler import BasePermissionHandler

# Define TypeVar for the decorator
F = TypeVar("F", bound=Callable[..., Any])

# Parameter name for passing agent role
AGENT_ROLE_PARAM = "agent_iam_role"


class NoOpTool(BaseTool):
    """A No-Op Tool that does nothing when permission is denied."""

    name: Optional[str] = "NoOpTool"
    description: Optional[str] = "This tool is used when permission is denied."

    def _run(self) -> Any:
        """Run the tool with proper argument handling.

        Args:
            args: Dictionary of positional arguments
            kwargs: Dictionary of keyword arguments
            tool_kwargs: Additional tool-specific keyword arguments
        """
        # Create a structured response that clearly indicates permission denial
        return {
            "status": "permission_denied",
            "error": "PermissionError",
            "message": (
                "Access Denied: You do not have permission to use this tool.\n\n"
                "Alternative Actions:\n"
                "1. Skip calling this tool and continue with available information\n"
            ),
            "data": None,  # No data available due to permission denial
            "recommendations": [
                "skip calling this tool and continue with available information",
            ],
        }


class NoOpTask(Task):
    """A No-Op Task that does nothing when permission is denied."""

    def __init__(self, *args, **kwargs):
        # Ensure required fields are present
        if "description" not in kwargs:
            kwargs["description"] = "Permission denied task"
        if "expected_output" not in kwargs:
            kwargs["expected_output"] = "Error message indicating permission denial"
        # Forward all arguments to parent Task constructor
        super().__init__(*args, **kwargs)

    def execute_sync(self, *args, **kwargs) -> TaskOutput:
        return self._create_noop_output()

    def execute_async(self, *args, **kwargs) -> Future[TaskOutput]:
        future = Future()
        future.set_result(self._create_noop_output())
        return future

    def _create_noop_output(self) -> TaskOutput:
        """Helper method to create a TaskOutput with default values for a No-Op task."""
        agent = self.agent.role if self.agent else "NoOpAgent"

        # Create a detailed, structured output that helps agents understand and adapt
        output = (
            "Access Denied: You do not have permission to execute this task.\n\n"
            "Alternative Actions:\n"
            "1. Skip calling this task and continue with available information\n"
        )

        return TaskOutput(
            description=self.description,
            raw=output,
            pydantic=None,
            json_dict={
                "status": "permission_denied",
                "agent": agent,
                "message": {
                    "message": "You do not have permission to execute this task.",
                    "recommendations": [
                        "skip calling this task and continue with available information",
                    ],
                },
            },
            agent=agent,
            output_format=OutputFormat.RAW,
        )


class CrewAIPermissionHandler(BasePermissionHandler):
    """CrewAI-specific permission handler implementation."""

    def __init__(self, target_type: Type):
        super().__init__()  # Initialize base class which sets up tracer
        self.identity_manager = IdentityManager.get_instance()
        self.target_type = target_type

    def check_permission(self, scope: str, agent_role: str) -> bool:
        token = self.get_token(agent_role)
        return self.identity_manager.validate_scope(token, scope)

    def handle_no_permission(
        self, scope: str, agent_role: str, context_type: Type, *args, **kwargs
    ) -> Any:
        """Handle permission denial based on the type.

        Args:
            scope: The required scope
            agent_role: The agent's role
            context_type: The type of the decorated function's first argument
            args: Original positional arguments from the decorated function
            kwargs: Original keyword arguments from the decorated function
        """
        # For tools, always return NoOpTool
        if self.target_type == type(BaseTool):
            return NoOpTool()

        # For tasks, create NoOpTask
        task_args = args[1:] if len(args) > 1 else ()
        return NoOpTask(*task_args, **kwargs)

    def get_token(self, agent_role: str) -> Optional[str]:
        return self.identity_manager.get_token(agent_role)

    def create_decorator(self, scope: str, pass_token: bool = False) -> Callable:
        """Override to capture kwargs before permission check."""
        base_decorator = super().create_decorator(scope, pass_token)

        def decorator(func: F) -> F:
            wrapped = base_decorator(func)

            @functools.wraps(wrapped)
            def wrapper(*args, **kwargs):
                try:
                    if not self.check_permission(scope, kwargs[AGENT_ROLE_PARAM]):
                        # Get the context from the first argument if it exists
                        context = args[0] if args else None
                        return self.handle_no_permission(
                            scope,
                            kwargs[AGENT_ROLE_PARAM],
                            type(context) if context else None,
                            *args,
                            **kwargs
                        )
                    return wrapped(*args, **kwargs)
                finally:
                    kwargs.clear()

            return cast(F, wrapper)

        return decorator


# Create singleton instances of the permission handlers
_task_permission_handler = CrewAIPermissionHandler(type(Task))
_tool_permission_handler = CrewAIPermissionHandler(type(BaseTool))


def requires_task_scope(scope: str, pass_token: bool = False):
    """Decorator that validates scope requirements for CrewAI framework."""
    return _task_permission_handler.create_decorator(scope, pass_token)


def requires_tool_scope(scope: str, pass_token: bool = False):
    """Decorator that validates scope requirements for CrewAI framework."""
    return _tool_permission_handler.create_decorator(scope, pass_token)
