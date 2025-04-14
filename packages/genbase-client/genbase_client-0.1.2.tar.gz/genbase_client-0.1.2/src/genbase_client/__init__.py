# src/genbase_agent_client/__init__.py

# Expose the main components for easy import by Kit developers
from .base_agent import BaseAgent, tool, collect_tools
from .types import AgentContext, IncludeOptions, ProfileStoreFilter, ProfileStoreRecord


__version__ = "0.1.0" # Keep in sync with pyproject.toml

__all__ = [
    "BaseAgent",
    "tool",
    "collect_tools",
    "AgentContext",
    "IncludeOptions",
    "ProfileStoreFilter",
    "ProfileStoreRecord",
    "__version__",
]