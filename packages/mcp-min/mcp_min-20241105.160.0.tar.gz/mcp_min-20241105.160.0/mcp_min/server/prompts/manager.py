"""Prompt management functionality."""

from typing import Any

from .base import Message, Prompt


class PromptManager:
    """Manages FastMCP prompts."""

    def __init__(self):
        self._prompts: dict[str, Prompt] = {}

    def get_prompt(self, name: str) -> Prompt | None:
        """Get prompt by name."""
        return self._prompts.get(name)

    def list_prompts(self) -> list[Prompt]:
        """List all registered prompts."""
        return list(self._prompts.values())

    def add_prompt(
        self,
        prompt: Prompt,
    ) -> Prompt:
        """Add a prompt to the manager."""

        # Check for duplicates
        existing = self._prompts.get(prompt.name)
        if existing:
            return existing

        self._prompts[prompt.name] = prompt
        return prompt

    async def render_prompt(self, name: str, arguments: dict[str, Any] | None = None) -> list[Message]:
        """Render a prompt by name with arguments."""
        prompt = self.get_prompt(name)
        if not prompt:
            raise ValueError(f"Unknown prompt: {name}")

        return await prompt.render(arguments)
