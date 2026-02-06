"""
Agent 6: Consistency Checker
=============================
Responsibility: Evaluate the generated story for INTERNAL CONSISTENCY.
This is the QA agent — it checks for plot holes, character inconsistencies,
world-rule violations, and tonal shifts.

Why this agent exists (and why it's CRUCIAL):
  LLMs are creative but inconsistent. Without a checking agent, you get:
  - Characters acting out of their established personality
  - World rules being violated (e.g., a character using tech that doesn't exist)
  - Plot holes where cause-and-effect breaks down
  - Tonal whiplash (comedy in a tragic moment)

  This agent acts as a UNIT TEST for the narrative. It reads the story
  against the world rules and character specs and flags violations.

Design note: Low temperature (0.2) — this is a strict analytical task.
We want the checker to be pedantic and thorough, not forgiving.
"""

from agents.base_agent import BaseAgent


class ConsistencyCheckerAgent(BaseAgent):
    NAME = "Consistency Checker"
    ROLE = "QA agent — checks story for internal consistency and coherence"

    SYSTEM_PROMPT = """You are a meticulous story editor and continuity checker.

Your job is to read a generated story and CHECK IT AGAINST the established
world rules, character specifications, and plot outline. You are looking for
PROBLEMS — inconsistencies, violations, plot holes, and tonal issues.

You must check the following dimensions:

1. **WORLD RULE COMPLIANCE** — Does anything happen that violates the
   established rules of the target universe? (e.g., technology that doesn't
   exist, social norms being ignored without consequence)

2. **CHARACTER CONSISTENCY** — Does each character behave according to their
   established personality, motivation, and speech patterns? Do any characters
   act "out of character" without narrative justification?

3. **PLOT LOGIC** — Does the cause-and-effect chain hold up? Are there plot
   holes? Does the resolution follow logically from the setup?

4. **THEMATIC FIDELITY** — Are the core themes from the source material
   preserved? Does the emotional architecture match? Are any themes lost
   or distorted?

5. **TONAL CONSISTENCY** — Is the tone maintained throughout? Are there
   jarring shifts? Does the humor (if any) fit the genre?

6. **CULTURAL SENSITIVITY** — Are there any stereotypical or disrespectful
   portrayals? Does the adaptation handle cultural elements with care?

For each issue found, provide:
- **ISSUE**: What the problem is
- **LOCATION**: Where in the story it occurs
- **SEVERITY**: Critical / Major / Minor
- **SUGGESTED FIX**: How to resolve it

End with:
- **OVERALL SCORE**: Rate the story 1-10 on consistency
- **VERDICT**: PASS (score >= 7) or NEEDS REVISION (score < 7)
- **SUMMARY**: 2-3 sentences on overall quality

Be thorough and critical. It's better to flag a non-issue than miss a real problem."""

    def build_prompt(self, context: dict) -> str:
        world_building = context.get("world_building", "")
        character_mapping = context.get("character_mapping", "")
        plot_outline = context.get("plot_outline", "")
        story = context.get("story", "")

        return f"""Check the following story for consistency against its specifications.

WORLD RULES (what the world allows):
{world_building}

CHARACTER SPECS (who they are and how they should behave):
{character_mapping}

PLOT OUTLINE (what should happen):
{plot_outline}

GENERATED STORY (what to check):
{story}

Perform a thorough consistency check. Be critical but fair."""

    def _get_temperature(self) -> float:
        return 0.2  # strict, analytical

    def _get_max_tokens(self) -> int:
        return 3000
