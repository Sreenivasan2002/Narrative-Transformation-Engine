"""
Agent 3: Character Mapper
=========================
Responsibility: Transform each source character into their target-universe
equivalent while preserving their FUNCTION and ESSENCE.

Why this agent exists:
  Character mapping is the hardest part of narrative transformation.
  A naive approach just renames characters. A good approach asks:
  "What kind of person in THIS world would face the SAME dilemmas
  and make the SAME choices for the SAME reasons?"

  Karna isn't just "a loyal warrior" — he's someone whose identity was
  denied by the establishment, who was given dignity by the wrong side,
  and now fights against his own blood out of gratitude-debt. In GTA,
  that's a kid from the projects who was rejected by the Pandava family
  but taken in by Duryodhana's crew. Same soul, different skin.

Design note: Medium-high temperature (0.7) — needs creativity for
character voice, but must stay consistent with the world rules.
"""

from agents.base_agent import BaseAgent


class CharacterMapperAgent(BaseAgent):
    NAME = "Character Mapper"
    ROLE = "Transforms characters while preserving their essence"

    SYSTEM_PROMPT = """You are a character design expert specializing in narrative adaptation.

Your job is to transform characters from a source story into a target universe while
preserving what makes them MATTER to the story.

For each character, you must answer THREE questions:
1. What kind of person in the TARGET world would face the same dilemmas?
2. What would make them make the same choices?
3. What gives them the same emotional impact on the audience?

For each character, provide:

1. **ORIGINAL → NEW** — Name mapping and one-line concept
2. **NEW IDENTITY** — Who they are in this world (background, job, status)
3. **PRESERVED ESSENCE** — What's the same: their core conflict, motivation, flaw
4. **TRANSFORMED DETAILS** — What changed and WHY it works in the new context
5. **SIGNATURE TRAITS** — Unique details that make them feel alive in the new world
   (appearance, speech patterns, habits, vehicle, weapon of choice)
6. **KEY RELATIONSHIPS** — How they relate to other transformed characters
7. **CHARACTER VOICE** — A sample line of dialogue that captures their personality

CRITICAL RULES:
- Don't just rename. REIMAGINE.
- Every character must feel like they BELONG in the target world.
- Their arc must serve the same narrative function as in the source.
- Give each character a distinctive voice — they shouldn't all sound the same.
- The tragic characters must remain tragic. The complex ones must stay complex."""

    def build_prompt(self, context: dict) -> str:
        source_analysis = context.get("source_analysis", "")
        world_building = context.get("world_building", "")
        source_data = context.get("source_material", "")

        return f"""Transform the characters from the source material into the target universe.

SOURCE CHARACTERS AND THEIR NARRATIVE FUNCTIONS:
{source_analysis}

ORIGINAL CHARACTER DATA:
{source_data}

TARGET UNIVERSE (the world they now exist in):
{world_building}

Create vivid, believable character transformations. Each one should feel like
they were BORN in this world, not transplanted into it."""

    def _get_temperature(self) -> float:
        return 0.7

    def _get_max_tokens(self) -> int:
        return 4000
