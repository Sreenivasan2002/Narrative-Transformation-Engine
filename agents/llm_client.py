"""
LLM Client — Thin wrapper around OpenAI API.

Design decision: Centralize all LLM calls here so that:
  1. We can swap providers (Anthropic, Gemini) without touching agent code
  2. We control temperature/model per-call for reproducibility
  3. We can add retry logic, logging, and token tracking in one place
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)  # override=True ensures .env takes precedence over system env vars


class LLMClient:
    """Manages all interactions with the LLM provider."""

    def __init__(self, model: str = "gpt-4o-mini"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file")
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.total_tokens_used = 0  # track cost across the pipeline

    def call(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        json_mode: bool = False,
    ) -> str:
        """
        Single LLM call with explicit system/user separation.

        Args:
            system_prompt: Defines the agent's role and constraints
            user_prompt:   The actual task/data for this step
            temperature:   0.0 = deterministic, 1.0 = creative
            max_tokens:    Output length cap
            json_mode:     If True, force JSON response format

        Returns:
            The LLM's response as a string
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = self.client.chat.completions.create(**kwargs)

        # Track token usage for cost awareness
        if response.usage:
            self.total_tokens_used += response.usage.total_tokens

        return response.choices[0].message.content

    def call_with_context(
        self,
        system_prompt: str,
        context_messages: list[dict],
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4000,
    ) -> str:
        """
        LLM call with multi-turn context — used when an agent needs
        to see prior conversation (e.g., evaluator reviewing all outputs).
        """
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(context_messages)
        messages.append({"role": "user", "content": user_prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        if response.usage:
            self.total_tokens_used += response.usage.total_tokens

        return response.choices[0].message.content
