"""
Base Agent — Abstract foundation for all specialist agents.

Architecture pattern: Each agent follows a simple contract:
  1. Has a NAME and ROLE (used in logging and orchestration)
  2. Has a SYSTEM_PROMPT (defines its personality and constraints)
  3. Implements `build_prompt(context)` to construct its specific query
  4. Implements `run(context)` to execute and return results
  5. Optionally implements `parse_output(raw)` for structured extraction

This design makes agents composable — the orchestrator doesn't care
about internal logic, only the input/output contract.
"""

import sys, os
from abc import ABC, abstractmethod
from agents.llm_client import LLMClient
from rich.console import Console
from rich.panel import Panel

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

console = Console(force_terminal=True)


class BaseAgent(ABC):
    """Abstract base class for all pipeline agents."""

    NAME: str = "BaseAgent"
    ROLE: str = "Generic agent"
    SYSTEM_PROMPT: str = ""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    @abstractmethod
    def build_prompt(self, context: dict) -> str:
        """
        Construct the user-side prompt from pipeline context.
        Each agent decides what it needs from the shared context dict.
        """
        pass

    def run(self, context: dict) -> str:
        """
        Execute the agent: build prompt → call LLM → return result.
        Also handles logging via Rich for a clean terminal experience.
        """
        console.print(
            Panel(
                f"[bold cyan]{self.ROLE}[/bold cyan]",
                title=f"🤖 Agent: {self.NAME}",
                border_style="blue",
            )
        )

        user_prompt = self.build_prompt(context)
        result = self.llm.call(
            system_prompt=self.SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=self._get_temperature(),
            max_tokens=self._get_max_tokens(),
            json_mode=self._use_json_mode(),
        )

        console.print(f"  [green]✓[/green] {self.NAME} completed.\n")
        return result

    def _get_temperature(self) -> float:
        """Override in subclasses. Analytical agents use low temp, creative agents use higher."""
        return 0.7

    def _get_max_tokens(self) -> int:
        """Override in subclasses based on expected output length."""
        return 4000

    def _use_json_mode(self) -> bool:
        """Override to True for agents that must return structured JSON."""
        return False
