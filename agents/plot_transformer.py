"""
Agent 4: Plot Transformer
==========================
Responsibility: Reimagine the plot skeleton in the target universe,
using the mapped characters and world rules.

Why this agent exists:
  Plot transformation is where the rubber meets the road. The source
  analyzer gave us the SKELETON. The world builder gave us the STAGE.
  The character mapper gave us the CAST. Now we need to choreograph
  the DANCE — making the plot feel inevitable within the new world.

  The key insight: we don't transplant events, we transplant FUNCTIONS.
  The dice game's function isn't "gambling" — it's "the hero's code of
  honor is used as a weapon against him, causing him to lose everything."
  In GTA, that could be a rigged poker night at a VIP casino, or a
  contract deal with hidden clauses.

Design note: This agent works in a structured format — act by act,
scene by scene — to ensure completeness and coherence.
"""

from agents.base_agent import BaseAgent


class PlotTransformerAgent(BaseAgent):
    NAME = "Plot Transformer"
    ROLE = "Reimagines the plot structure in the target universe"

    SYSTEM_PROMPT = """You are a master screenwriter specializing in narrative adaptation and genre translation.

Your job is to take a source plot skeleton and reimagine it in a target universe,
using the provided characters and world rules.

CRITICAL PRINCIPLE: Transform FUNCTIONS, not events.
- Don't ask "What's the equivalent of a dice game?"
- Ask "What situation in this world would exploit the hero's sense of honor to strip away everything they have?"

Structure your output as a SCENE-BY-SCENE plot outline:

**ACT 1: SETUP** (3-4 scenes)
Establish the world, introduce key characters, plant the seeds of conflict.

**ACT 2A: ESCALATION** (3-4 scenes)
The conflict grows. The point-of-no-return event happens. Alliances shift.

**ACT 2B: EXILE & PREPARATION** (3-4 scenes)
The heroes regroup, train, build alliances. Tension builds.

**ACT 3: CONFRONTATION & AFTERMATH** (3-4 scenes)
The climactic conflict, key deaths/defeats, and the bittersweet resolution.

For EACH scene provide:
1. **Scene title** (evocative, GTA-mission-style)
2. **Location** (from the world building)
3. **Characters involved**
4. **What happens** (2-3 sentences)
5. **Source parallel** (what original event/function this preserves)
6. **Emotional beat** (what the audience should feel)

RULES:
- Every scene must feel natural in the target world — no forced parallels
- Maintain cause-and-effect logic — each scene should set up the next
- The emotional architecture from the source must be preserved in order
- Key moments of the source must have equally powerful equivalents
- No deus ex machina — resolutions must follow the world's rules"""

    def build_prompt(self, context: dict) -> str:
        source_analysis = context.get("source_analysis", "")
        world_building = context.get("world_building", "")
        character_mapping = context.get("character_mapping", "")

        return f"""Reimagine the source story's plot in the target universe.

SOURCE STORY STRUCTURE AND THEMES:
{source_analysis}

TARGET UNIVERSE:
{world_building}

REIMAGINED CHARACTERS:
{character_mapping}

Create a scene-by-scene plot outline that feels inevitable in this world.
Every beat should feel like it belongs — not transplanted, but native."""

    def _get_temperature(self) -> float:
        return 0.7

    def _get_max_tokens(self) -> int:
        return 4000
