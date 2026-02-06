"""
Narrative Transformation Agentic System
========================================
Multi-agent pipeline for reimagining classic stories in new universes.

Each agent is a specialist with a defined role, system prompt, and output schema.
The orchestrator coordinates them in a DAG (directed acyclic graph) pattern,
passing context forward so each agent builds on the previous one's work.
"""

from agents.base_agent import BaseAgent
from agents.llm_client import LLMClient
from agents.orchestrator import Orchestrator

__all__ = ["BaseAgent", "LLMClient", "Orchestrator"]
