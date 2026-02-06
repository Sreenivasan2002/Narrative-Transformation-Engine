"""
Agent 1: Source Analyzer
========================
Responsibility: Deconstruct the source material into its fundamental
narrative building blocks — themes, character archetypes, plot structure,
emotional beats, and symbolic elements.

Why this agent exists separately:
  Before we can transform anything, we need a deep structural understanding
  of WHAT makes the source story work. This is the "understand before you
  build" principle. The output of this agent becomes the blueprint that
  all subsequent agents reference.

Design note: Temperature is set LOW (0.3) because this is an analytical
task, not a creative one. We want consistent, thorough deconstruction.
"""

from agents.base_agent import BaseAgent


class SourceAnalyzerAgent(BaseAgent):
    NAME = "Source Analyzer"
    ROLE = "Deconstructs source material into narrative primitives"

    SYSTEM_PROMPT = """You are a narrative analyst specializing in comparative mythology and story structure.

Your job is to DECONSTRUCT a source story into its fundamental building blocks.
You must extract elements that are TRANSFERABLE across contexts — not surface details,
but the deep structures that make the story resonate.

For each element you extract, explain WHY it matters to the story's impact.

Output the following sections clearly:

1. **CORE THEME DNA** — The 3-5 irreducible themes. For each: what it is, why it's essential,
   and what happens to the story if you remove it.

2. **CHARACTER ARCHETYPES** — For each major character: their archetype (mentor, trickster,
   tragic hero, etc.), their FUNCTION in the plot (what do they cause to happen?),
   and their essential internal conflict.

3. **PLOT SKELETON** — The story reduced to 6-8 universal plot beats
   (using the framework: Status Quo → Disruption → Escalation → Point of No Return →
   Crisis → Climax → Resolution → Aftermath).

4. **EMOTIONAL ARCHITECTURE** — The sequence of emotions the audience MUST feel, in order.
   This is the "feeling blueprint" that must survive the transformation.

5. **SYMBOLIC ELEMENTS** — Objects, locations, or rituals that carry metaphorical weight.
   What do they represent abstractly?

6. **POWER DYNAMICS** — Who has power, who wants it, how it shifts. Map the power flows.

Be thorough, analytical, and specific. Reference actual story details."""

    def build_prompt(self, context: dict) -> str:
        source_data = context.get("source_material", "")
        return f"""Deconstruct the following source material into its narrative building blocks.

SOURCE MATERIAL:
{source_data}

Perform a deep structural analysis. Extract everything that a story transformer
would need to preserve when reimagining this in a completely different universe."""

    def _get_temperature(self) -> float:
        return 0.3  # analytical, not creative

    def _get_max_tokens(self) -> int:
        return 4000
